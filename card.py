class Card:
    suites=['Club','Diamonds','Hearts','Spades']
    display_values={1:'Ace',11:'Jack',12:'Queen',13:'King'}
    
    def __init__(self,value,suite):
        self._value  = value
        self._suite  = suite
    
    def __str__(self):
        return '{0} of {1}'. format(self.name(),self.suite())
        
    def suite(self):
        return self.__class__.suites[self._suite]
    
    def name(self):
        if self.__class__.display_values.has_key(self._value):
            return self.__class__.display_values[self._value]
        return self._value
    
    def value(self):
        if self._value==1:
            return [1,11]
        if self._value>10:
            return [10]
        else:
            return [self._value]