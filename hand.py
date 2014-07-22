from copy import copy
from card import Card

class Hand:
    def __init__(self, bet):
        self._cards = []
        self._bet   = bet
        self._eval  = 0
        self._split = True
        self._double = True
        
    def insert(self,card):
        if card:
            self._cards.append(card)
            self._eval = self.evaluate()
        else:
            raise AttributeError('None Type passed for Insertion')
    
    def _evaluate(self,cards,value):
        cards = copy(cards)
        if not cards:
            if value>21:
                return -1
            else:
                return value
        current_card = cards.pop()
        return max( self._evaluate(cards,(value+card_value)) for card_value in current_card.value() )
    
    def evaluate(self):
        return self._evaluate(self._cards,0)

    def isBlackjack(self):
        if self._eval is 21 and len(self._cards) is 2:
            return True
        else:
            return False
    
    def collect_bet(self):
        amount = self._bet
        self._bet = 0
        return amount
    
    def describe(self):
        hands = ''
        for card in self._cards:
            hands = hands +'\t' +card.__str__()+']'
        eval  = 'Value : {0}\nBet : {1}'.format(str(self.evaluate()),self._bet)
        seperator ='*'*40
        return (hands+'\n'+eval+'\n'+seperator)
    
    def __str__(self):
        hands = ''
        for card in self._cards:
            hands = hands + '\t'+ card.__str__()+ ']'
        return hands
    
    def can_split(self):
        return self._split
        
    def can_double(self):
        return self._double
    
    def cannot_double(self):
        self._split = False
        self._double = False
    
    def get_bet(self):
        return self._bet
        
    def add_bet(self, more_bet):
        self._bet += more_bet
        
    def isBlackjack(self):
        if self._eval is 21 and len(self._cards) is 2:
            return True
        else:
            return False
    
class SplitHand(Hand):
    def __init__(self, bet):
        self._cards = []
        self._bet   = bet
        self._eval  = 0
        self._split = False

        # We allow Double-down on splits
        self._double = True

