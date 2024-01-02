from random import shuffle
from card import *

#We create a class called Deck. To this deck we add all 81 unique cards once.
class Deck:
    def __init__(self, cards_folder=""):
        self.cards=[]
        self.cards_folder = cards_folder
        for symbol in range(3):
            for color in range(3):
                for shade in range(3):
                    for number in range(3):
                        card=Card(number,color,symbol,shade, cards_folder)
                        self.cards.append(card)

    #We also define a str method which prints the names of the cards in the order they are in the deck.
    #Every card is printed on a new line, but it still is just one string.
    def __str__(self):
        stringdeck=[]
        for card in self.cards:
            stringdeck.append(str(card))
        return "\n".join(stringdeck)
    
    #We define a method that removes a card from the deck.
    def pop_card(self):
        return self.cards.pop()
    
    #We define a method that adds a card to the deck.
    def add_card(self, card):
        self.cards.append(card)

    #We define a method called shuffle, which shuffles the deck.
    #We can call this function with Deck.shuffle() in main.
    def shuffle(self):
        shuffle(self.cards)

    #We define a method called move_cards. 
    #This method is used to move an amount of cards during the game. 
    def move_cards(self,move_to,amount):
        for i in range(amount):
            move_to.add_card(self.pop_card())
