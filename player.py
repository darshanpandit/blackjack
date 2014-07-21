class Player:
    def __init__(self, name):
        self.id = name
        self.credit = 100
        self.ptype = 'player'
    
    def bet(self,amount):
        if self.can_bet(amount):
            self.credit = self.credit - amount
            return amount
        else:
            raise ValueError('Insufficient Credit for the player')
    
    def can_bet(self,amount):
        if amount<self.credit:
            return True
        else:
            return False
    
    def collect_bet(self,amount):
        self.credit = self.credit + amount
        
#TODO: Error handling for Negative Amounts passed as parameters

class Dealer(Player):
    def __init__(self):
        self.id = 'dealer'
        self.credit = float('inf')
        self.ptype = 'dealer'

#Dealer is not allowed to have infinity as a loss. So we wont our House will always be in finite losses :)
#Overload method to find out how much profit the House makes in a set of games