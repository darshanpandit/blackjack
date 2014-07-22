from player import *
from horseshoe import Horseshoe
from movegenerator import MoveGenerator
from utilities import *
from hand import Hand
from card import Card

class Board:
    def __init__(self, PLAYER_COUNT=1, NUMBER_OF_DECKS=1, MINIMUM_BET=1):
        self._dealer = Dealer()
        self._players = [Player(x) for x in xrange(PLAYER_COUNT)]
        self._shoe = Horseshoe(NUMBER_OF_DECKS)
        self._MINIMUM_BET = MINIMUM_BET
        self._move_generator = MoveGenerator(self._shoe)
    
    def play(self):
        players = self._players
        shoe = self._shoe
        #movegen = MoveGenerator(shoe)
                    
        while True:
            if players:
                eliminated_players = []
                for player in players:
                    if not player.can_bet(self._MINIMUM_BET):
                        eliminated_players.append(player)
                        players.remove(player)
                if eliminated_players:
                    print '<'*60
                    print 'Following players cannot bet any further and are removed from table:'
                    for player in eliminated_players:
                        print 'Player {0}'.format(player.id)
                    print '>'*60
                    pass
                else:
                    #Collect bets from each player
                    bets = self._collect_bets(players)
                    
                    #Initialize them a hand for the bet they made
                    hands = [ [player,Hand(bet)] for player, bet in zip(players, bets) ]
                    dealer_hand = Hand(0)
                    
                    
                    print '#'*60
                    print 'First Card will be served'
                    print '#'*60
                    #Serve them their first card
                    [hand.insert(shoe.draw()) for player,hand in hands]
                    #Serve the dealer the first card
                    #TODO When we have limits for dealer, break conditions here
                    dealer_hand.insert(shoe.draw())
                    #Print state for each player
                    for player,hand in hands:
                        print 'Player {0} : Your Cards are :'.format(player.id)
                        print hand
                        print '*'*50

                    print 'Dealers Hand :'
                    print dealer_hand
                    print '*'*50

                    
                    print '#'*60
                    print 'Next Card will be served'
                    print '#'*60
                    #Serve them their second card
                    [hand.insert(shoe.draw()) for player,hand in hands]
                    dealer_hand.insert(shoe.draw())
                    
                    for player,hand in hands:
                        print 'Player {0} : Your Cards are :'.format(player.id)
                        print hand

                    print '#'*60
                    
                    final_hands =[]
                    
                    for player,hand in hands:
                        for ret_hand in self._user_action(player,hand):
                            final_hands.append(ret_hand)
                    
                    #Show Dealer's Hand 
                    print '#'*60
                    print 'Dealer\s Hand'
                    print dealer_hand  

                    while True:
                        dealer_value = dealer_hand.evaluate()
                        if dealer_value in range(1,17):
                            self._move_generator._hit(self._dealer,dealer_hand)
                        else:
                            break

                    print '#'*60
                    print 'Dealer\'s Final Hand'
                    print dealer_hand     
                    #Print Dealer's state 
                    
                    for player,hand in final_hands:
                        payoff_code = self._compare(hand,dealer_hand)
                        value = self._payoff(player, hand, payoff_code)
                        
                        if payoff_code >  1:
                            print 'Player {0} had a blackjack. Gets Back {1}'.format(player.id, value)
                        if payoff_code == 1:
                            print 'Player {0} had a win.       Gets Back {1}'.format(player.id, value)
                        if payoff_code == 0:
                            print 'Player {0} had a push.      Gets Back {1}'.format(player.id, value)
                        if payoff_code <  0:
                            print 'Player {0} had a loss.      Loses     {1}'.format(player.id, value)

                        #collect used cards
                        for card in hand._cards:
                            self._shoe.collect(card)    
                    
                    
            else:
                print 'Table is now empty. Now closing the table.'
                break
    
    def _collect_bets(self,players):
        bets = []
        for player in players:
            while True:
                try:
                    suggested_bet = int(raw_input("Hi Player {0}. Enter your bet in range({1},{2}) : ".format(player.id, self._MINIMUM_BET,player.credit)))
                    print '*'*50
                    #suggested_bet = 10
                    if suggested_bet<0 or not player.can_bet(suggested_bet):
                        pass
                    else:
                        bets.append(player.bet(suggested_bet))
                        break
                except ValueError:
                    pass
        return bets
    
    def _user_action(self,player,hand):
        while True:
            print 'Player {0} : Your Hand is :'.format(player.id)
            print hand.describe()

            methods = [meth for meth in self._move_generator.generate_possible_methods(player,hand)]
            
            #print methods and take input from user to invoke appropriate method
            print 'Player {0} :  What do you want to do?'.format(player.id)
            i=0
            for method_name, method in methods:
                print '{0} : {1}'.format(i,method_name)
                i+=1    

            #Continue taking input till we have a valid input
            choice =0
            while True:
                try:
                    input = int(raw_input("Please select the action_number : "))
                    if input in range(len(methods)):
                        choice = input
                        break
                except ValueError:
                    pass
            try:
                #call the method
                #method call will raise StopIteration upon bust or stand move
                child_hands = methods[choice][1](player,hand)
                
                #Will be null unless split is called
                if child_hands:
                    processed_hands = []
                    for child_hand in child_hands:
                        #recursive call for each child_hand from split
                        to_process_tuples = self._user_action(player,child_hand)
                        
                        #child_hands added to list
                        for tup in to_process_tuples:
                            processed_hands.append(tup)

                    #final list 
                    return processed_hands
        
            except StopIteration:
                print '^'*50
                print 'Player {0} : Your Final Hand : '
                print hand
                print '^'*50
                
                return [[player,hand]]
                
    #Compares hands. Returns -1,0,1 or 2    
    def _compare(self,player_hand, dealer_hand):
        player_value = player_hand.evaluate()
        dealer_value = dealer_hand.evaluate()
        
        if dealer_hand.isBlackjack():
            if player_hand.isBlackjack():
                return 0
            else:
                return -1
        else:
            if player_hand.isBlackjack():
                return 2
            if player_value > dealer_value:
                return 1
            if player_value == dealer_value:
                return 0
            else:
                return -1

    #Calculates payoff for the bet placed on the hand based on the code
    #Updates the bet in hand and then if code is >=0, player collects the money back else dealer gets it
    def _payoff(self,player,hand,code):
        bet = hand.get_bet()
        dealer = self._dealer
        if code>=0:
            #3:2 payoff for blackjack
            if code == 2:
                bet_amount = dealer.bet(bet*1.5)
            
            #1:1 Regular win for the player
            if code == 1:
                bet_amount = dealer.bet(bet)
            
            #push - no payoffs
            if code == 0:
                bet_amount = 0
            hand.add_bet(bet_amount)
            bet = hand.get_bet()

            player.collect_bet(hand.collect_bet())
        else:
            #player loses
            dealer.collect_bet(hand.collect_bet())
        return bet

if __name__ ==  '__main__':
    board = Board(2)
    board.play()
    
