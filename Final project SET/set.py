from card import *
from table import *

#We create a class set. This is a list of cards (not necessarily a valid set).
class Set():
    def __init__(self):
        self.cards=[]

   # def add_card(self, (Card)card):
    #    self.cards.append(card)

    def add_card(self, list):
        for i in range(len(list)):
            self.cards.append(list[i])

    def create_set(self, string, table):
        self.cards=[]
        try:
            numbers = string.split(",")
        except ValueError:
            print("This is not a valid format, try again")
            return
    
        if len(numbers) != 3:
            print("This is not a valid format, try again")
            return
        
        self.add_card([table.cards[int(numbers[0])-1], table.cards[int(numbers[1])-1], table.cards[int(numbers[2])-1]])


    

    