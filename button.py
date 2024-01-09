import pygame
from gameobject import *
from os import path
"""
A Button is a gameobject and the Button class inherits from Gameobject
It has a default (unpressed) image and no text.
It can also use a secondary (pressed) image, if the mouse is hovering
over the button.
"""
class Button(Gameobject):
    def __init__(self, screen=None, image_folder="", pressed_image="", unpressed_image="", center_position=(0,0)):
        # By default, the unpressed image is used
        Gameobject.__init__(self, screen, image_folder, unpressed_image, center_position)
        # Button also has a secondary image for "pressed" situations
        self.pressed_image = pygame.image.load(path.join(image_folder, pressed_image))
        self.pressed_imagerect = self.pressed_image.get_rect()
        self.pressed_imagerect.center = center_position
        # By default, the mouse is not hovering over the button
        self.hovering = False

    def draw(self):
        #Draw pressed or unpressed button on screen (depending where mouse is hovering)
        if self.hovering:
            # Mouse is above the button, use secondary image
            self.screen.blit(self.pressed_image, self.pressed_imagerect)
        else:
            # Mouse is not above the button, draw the default image
            Gameobject.draw(self)

    def update(self):
        # During update, check if the mouse is above the button or not
        self.check_hover()
    
    def check_hover(self):
        # Check if mouse is hovering over the button
        # Get mouse position
        x,y = pygame.mouse.get_pos()
        # Check if the mouse is colliding with the rectangle of the image
        if self.pressed_imagerect.collidepoint(x,y):
            # Yes, mouse is hovering over the button
            self.hovering=True
        else:
            # No, mouse is not hovering over the button
            self.hovering=False