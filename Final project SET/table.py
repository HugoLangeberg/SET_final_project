from card import *
from deck import *

#We create a class called Table. On the table, there are 12 or more cards.
#Table is the child of deck.
class Table(Deck):
#We define an init method to override the one in the Deck class.
    def __init__(self,deck):
        self.cards=[]
        deck.shuffle()
        deck.move_cards(self,12)

    #We draw the 12 cards from the table on the screen.
    def display_cards(self,screen):
        for i in range(len(self.cards)):
            x=50+(i%3)*100
            y=25+(i//3)*125
            self.cards[i].image_rect.x = x
            self.cards[i].image_rect.y = y
            screen.blit(self.cards[i].image, (x,y))

    #We define a method to replace 3 cards, a given set-object, with cards from the deck.
    def replace_cards(self,deck,set):
        for i in range(len(set.cards)):
            number_card=self.cards.index(set.cards[i])
            self.cards[number_card]=deck.pop_card()