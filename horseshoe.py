import random
from card import Card

class Horseshoe:
    def __init__(self, NUMBER_OF_DECKS=4):
        self._shoe = [Card(card_value,card_type) for card_value in xrange(1,14) for card_type in xrange(0,4)]*NUMBER_OF_DECKS
        self._ground    = []
        
        def draw_shoe():
            while True:
                while len(self._shoe)>0:
                    rand_number = random.randint(0,len(self._shoe)-1)
                    card = self._shoe[rand_number]
                    del self._shoe[rand_number]
                    yield card
                #raise TypeError
                # We collect all the used cards , reshuffle them and redistribute to continue the game.
                self._shoe = self._ground
                self._ground = []
        drawer = draw_shoe()
        
        def draw():
            return next(drawer)
        self.draw = draw
        
        def collect(card):
            self._ground.append(card)
            return self._ground
        self.collect = collect

