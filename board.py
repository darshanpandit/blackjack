from player import *
from horseshoe import Horseshoe
from movegenerator import MoveGenerator

class Board:
    def __init__(self, PLAYER_COUNT=1, NUMBER_OF_DECKS=2, MINIMUM_BET=1):
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
                eliminated_players =  [ players.pop(x) for x in xrange( len(players) ) if not players[x].can_bet(self._MINIMUM_BET) ]
                if eliminated_players:
                    print 'Following players cannot bet any further here and are removed from the table:\n{0}'.format(eliminated_players)
                    pass
                else:
                    #Collect bets from each player
                    bets = self._collect_bets(players)
                    
                    #Initialize them a hand for the bet they made
                    hands = [ [player,Hand(bet)] for player, bet in zip(players, bets) ]
                    dealer_hand = Hand(0)
                    
                    #Serve them their first card
                    [hand.insert(shoe.draw()) for player,hand in hands]
                    #Serve the dealer the first card
                    #TODO When we have limits for dealer, break conditions here
                    dealer_hand.insert(shoe.draw())
                    
                    #Print state for each player
                    
                    #Serve them their second card
                    [hand.insert(shoe.draw()) for player,hand in hands]
                    dealer_hand.insert(shoe.draw())
                    
                    final_hands =[]
                    
                    for player,hand in hands: 
                        list1 = self._user_action(player,hand)
                        [final_hands.append(final_hand) for final_hand in list1]
                        
                        
                    print dealer_hand     
                    #Print Dealer's state 
                    while dealer_hand.evaluate in range(1,17):
                        self._move_generator._hit(self._dealer,hand)
                        #Print Dealer's Hand
                        print dealer_hand()
                    for player,hand in final_hands:
                        payoff_code = self._compare(hand,dealer_hand)
                        self._payoff(player, dealer, hand, payoff_code)
                        
                        #collect used cards
                        for card in hand._cards:
                            self._shoe.collect(card)    
                    
                    
            else:
                print 'Table is now empty. Now closing the table.'
                break
    
    
    def _payoff(self,player,dealer,hand,code):
        bet = hand.get_bet()
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
            player.collect_bet(hand.collect_bet())
        else:
            #player loses
            dealer.collect_bet(hand.collect_bet())
    
    def _compare(self,player_hand, dealer_hand):
        player_value = player_hand.value()
        dealer_value = dealer_hand.value()
        
        if dealer_hand.isBlackjack():
            if player_hand.isBlackJack():
                return 0
            else:
                return -1
        else:
            if player_hand.isBlackJack():
                return 2
            if player_value > dealer_value:
                return 1
            if player_value == dealer_value:
                return 0
            else:
                return -1
    
    def _collect_bets(self,players):
        bets = []
        for player in players:
            while True:
                try:
                    suggested_bet = int(raw_input("Hello Player {0}. Please input your bet  Positive and >{1} ".format(player.id,  self._MINIMUM_BET)))
                    #suggested_bet = 10
                    if suggested_bet<0 or not player.can_bet(suggested_bet):
                        raise ValueError
                        #pass
                    else:
                        bets.append(player.bet(suggested_bet))
                        break
                except ValueError:
                    raise ValueError#pass
        return bets
    
    def _user_action(self,player,hand):
        try:
            while True:
                methods = [meth for meth in movegen.generate_possible_methods(player,hand)]
                #print methods and take input from user to invoke appropriate method
                print 'What do you want to do?\n'
                i=0
                for method_name, method in methods:
                    print '{0} : {1}'.format(i,method_name)
                    i+=1
                choice = -1
                while choice<0:
                    try:
                        input = int(raw_input("Please select the action_number : "))
                        #input = 0
                        if input in range(len(methods)):
                            choice = input
                    except ValueError:
                        pass
                temp = methods[choice][1](player,hand)
                
                #Busted
                if hand._eval<0:
                    raise StopIteration
                #Only Split returns a value. rest are silent and do not return
                if temp:
                    split_list = []
                    for split_hand in temp:
                        self._user_action(player,split_hand)
                        split_list.append([player,split_hand])
        except StopIteration:
            return [[player, hand]]
    
board = Board()
board.play()