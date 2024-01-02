import pygame
from os import path

#We create a class, called card. 
#Every card has 4 properties: number, symbol, color and shading.
class Card:
    #The init method takes an optional parameter for each property.
    #The default card is greendiamondempty1.
    #The default cards_folder is the path where all card images are located.
    #It is in the subdirectory 'cards' of the directory where the current card.py file is located
    def __init__(self, number=0, symbol=0, color=0, shade=0, cards_folder=""):
        self.number=number
        self.symbol=symbol
        self.color=color
        self.shade=shade
        self.cardname=(Card.color_names[self.color] +
                Card.symbol_names[self.symbol] +
                Card.shade_names[self.shade] +
                Card.number_names[self.number])
        #Load and resize image to right proportions
        self.image=pygame.transform.scale(pygame.image.load(path.join(cards_folder,self.cardname+".gif")),(60,100))
        self.image_rect=self.image.get_rect()



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
