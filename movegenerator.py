from player import Player
from hand import *
from card import Card
from horseshoe import *

class MoveGenerator:
    def __init__(self,shoe):
        self._shoe = shoe
    
    def _hit(self,player,hand):
        hand.insert(self._shoe.draw())
   
    def _stand(self,player, hand):
        raise StopIteration
    
    def _split(self,player,hand):
        
        hand1 = SplitHand(hand.get_bet())
        hand1.insert(hand._cards[0])
        
        hand2 = SplitHand(player.bet(hand.get_bet()))
        hand2.insert(hand._cards[1])
        
        return [hand1, hand2]
    
    def _double(self,player,hand):
        hand.set_can_double(False)
        hand.add_bet(player.bet(hand.get_bet()))
        self.hit(player,hand)
        
    
    def generate_possible_methods(self,player,hand):
        if hand is None:
            raise AttributeError('NoneType was passed as Hand Object')
        value = hand._eval
        if value<0:
            yield None
        else:
            yield ['Hit',self._hit]
            yield ['Stand',self._stand]
            if player.can_bet(hand.get_bet() and hand.can_double()):
                yield ['DoubleDown',self._double]
                
            #We allow splits on 10s
            if len(hand._cards) is 2 and hand.can_split() and hand._cards[0].value() == hand._cards[1].value() and player.can_bet(hand.get_bet()):
                yield ['Split',self._split]
            
            
                
