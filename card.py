import pygame
from gameobject import *
from os import path

"""
A Card is a gameobject and the Card class inherits from Gameobject
It has a default (backside) image and no text.

Every card has 4 properties: number, symbol, color and shading.

The properties alltogether make up the front image of the card.
The front image is blitted on top of the default (backside) image to
create the final Card image.

A Card has a 'move_effect', which enables it to move from one position
to another in N steps. This is taken care of in the update() method
"""
class Card(Gameobject):
    # Assign the valid values of the properties as class attributes.
    number_names=["1","2","3"]                  # The 3 possible numbers
    symbol_names=["diamond","oval","squiggle"]  # The 3 possible symbols
    color_names=["green","red","purple"]        # The 3 possible colors
    shade_names=["empty","filled","shaded"]     # The 3 possible shading types

    # The init method takes an optional parameter for each property.
    # The default card is greendiamondempty1.
    # The image_folder is the path where all images are located.
    # The default image is the backside of a card
    def __init__(self, number=0, symbol=0, color=0, shade=0, screen=None, image_folder="", center_position=(0,0)):
        # Initialize first part via the Gameobject
        Gameobject.__init__(self, screen, image_folder, FILE_CARD_BACKSIDE, center_position)
        # Initialize rest of Card specific properties
        self.number=number
        self.symbol=symbol
        self.color=color
        self.shade=shade
        self.is_moving = False
        self.delta_x = 0
        self.delta_y = 0
        self.framecount = 0
        self.stop_framecount = 10
        self.delay = 0
        self.from_position_number = -1

        self.cardname=(Card.color_names[self.color] +
                Card.symbol_names[self.symbol] +
                Card.shade_names[self.shade] +
                Card.number_names[self.number])
        # Load and resize the front image to right proportions
        self.image_front=pygame.transform.scale(pygame.image.load(path.join(image_folder,self.cardname+".gif")),(60,100))
        self.image_front_rect=self.image_front.get_rect()
        # Align this new front image over the existing default (backside) image
        self.align_new_image_center(self.image_front_rect)
        # Blit the front card on top of the default (backside) image
        self.image.blit(self.image_front, self.image_front_rect)
    
    def __str__(self):
        # This method returns the name of the card as a string.
        return self.cardname
    
    def update(self):
        if self.framecount == self.stop_framecount:
            # It is time to finish the movement of the card
            self.is_moving = False
            self.delta_x = 0
            self.delta_y = 0
            self.delay = 0
            self.framecount = 0
            self.stop_framecount = -1
            # Set the end position of this card
            self.set_center_position(self.to_position)
            
        if self.is_moving:
            if self.framecount >= self.delay:
                # Still moving, so update the X and Y coordinates of the center
                self.image_rect.centerx = self.from_position[0] + (self.framecount-self.delay)*self.delta_x
                self.image_rect.centery = self.from_position[1] + (self.framecount-self.delay)*self.delta_y
            self.framecount += 1

    def move_effect(self, from_position, to_position, steps, delay):
        # Move the card from one position to another position in N steps
        self.framecount = 0
        # Wait N frames before starting
        self.delay = delay
        # Card starts at frame0 with the from_position. It needs N+1 steps to get to the end position
        self.stop_framecount = delay + steps + 1
        # Indicate the card is moving
        self.is_moving = True
        # Store input parameters
        self.from_position = from_position
        self.to_position = to_position
        # Calculate delta_x an delta_y needed by each frame update
        self.delta_x = (to_position[0] - from_position[0]) / steps
        self.delta_y = (to_position[1] - from_position[1]) / steps
