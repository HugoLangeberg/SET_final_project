import pygame
from os import path

#We create a class, called card. 
#Every card has 4 properties: number, symbol, color and shading.
class Card:
    #The init method takes an optional parameter for each property.
    #The default card is greendiamondempty1.
    #The default cards_folder is the path where all card images are located.
    #It is in the subdirectory 'cards' of the directory where the current card.py file is located
    def __init__(self, number=0, symbol=0, color=0, shade=0, screen=None, image_folder=""):
        self.screen=screen
        self.number=number
        self.symbol=symbol
        self.color=color
        self.shade=shade
        self.is_moving = False
        self.delta_x = 0
        self.delta_y = 0
        self.framecount = 0
        self.stop_framecount = 10
        self.cardname=(Card.color_names[self.color] +
                Card.symbol_names[self.symbol] +
                Card.shade_names[self.shade] +
                Card.number_names[self.number])
        #Load and resize image to right proportions
        self.image=pygame.transform.scale(pygame.image.load(path.join(image_folder,self.cardname+".gif")),(60,100))
        self.image_rect=self.image.get_rect()
        self.image_backside = pygame.image.load(path.join(image_folder, "card_backside.png"))
        self.image_backside_rect = self.image_backside.get_rect()



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
    
    def draw(self):
        # Blit backside
        self.screen.blit(self.image_backside, self.image_backside_rect)
        # Do the same for the card front
        self.screen.blit(self.image, self.image_rect)
        

    def update(self):
        # Is it time to finish the movement of the card?
        if self.framecount == self.stop_framecount:
            self.is_moving = False
            self.delta_x = 0
            self.delta_y = 0
            self.set_center_position(self.to_position)
            
            
        if self.is_moving:
            self.image_rect.centerx = self.from_position[0] + self.framecount*self.delta_x
            self.image_rect.centery = self.from_position[1] + self.framecount*self.delta_y
            self.framecount += 1

        

        # Always align backside image with the actual image position
        self.image_backside_rect.center = self.image_rect.center


    def set_center_position(self, position):
        self.image_rect.center = position

    def move_effect(self, from_position, to_position, steps):
        self.framecount = 0
        self.stop_framecount = steps + 1
        self.is_moving = True
        self.from_position = from_position
        self.to_position = to_position
        self.delta_x = (to_position[0] - from_position[0]) / steps
        self.delta_y = (to_position[1] - from_position[1]) / steps


