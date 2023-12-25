import random
import pygame
import os

game_folder = os.path.dirname(__file__)  # Main folder of the game.
cards_folder = os.path.join(game_folder, 'cards')  # Subdir cards contains card images.
font_folder = os.path.join(game_folder, 'font')  # Subdir font contains style.

#We create a class, called card. 
#Every card has 4 properties: number, symbol, color and shading.
class Card:
    def __init__(self, number=0, symbol=0, color=0, shade=0):
        self.number=number
        self.symbol=symbol
        self.color=color
        self.shade=shade
        self.cardname=(Card.color_names[self.color] +
                Card.symbol_names[self.symbol] +
                Card.shade_names[self.shade] +
                Card.number_names[self.number])
        self.image=pygame.transform.scale(pygame.image.load(os.path.join(cards_folder,self.cardname+".gif")),(60,100))

#The init method takes an optional parameter for each property.
#The default card is greendiamondempty1.

#There are 3 possible numbers: 1, 2, 3.
#There are 3 possible symbols: diamond, oval, squiggle.
#There are 3 possible colors: green, red, purple.
#There are 3 possible shades: empty, shaded, filled.
#We assign these lists to class attributes.
    number_names=["1","2","3"]
    symbol_names=["diamond","oval","squiggle"]
    color_names=["green","red","purple"]
    shade_names=["empty","filled","shaded"]

#We define a str method which returns the name of the card as a string.
    def __str__(self):
        return self.cardname
        
#We create a class called Deck. To this deck we add all 81 unique cards once.
class Deck:
    def __init__(self):
        self.cards=[]
        for symbol in range(3):
            for color in range(3):
                for shade in range(3):
                    for number in range(3):
                        card=Card(number,color,symbol,shade)
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
        random.shuffle(self.cards)

#We define a method called move_cards. 
#This method is used to move an amount of cards during the game. 
    def move_cards(self,move_to,amount):
        for i in range(amount):
            move_to.add_card(self.pop_card())

#We create a class called Table. On the table, there are 12 or more cards.
#Table is the child of deck.
class Table(Deck):
#We define an init method to override the one in the Deck class.
    def __init__(self):
        self.cards=[]
        deck=Deck()
        deck.shuffle()
        deck.move_cards(self,12)
    

    