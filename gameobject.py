import pygame
from os import path
from settings import *

"""
Gameobject is a base class for all visible items, like buttons, cards etc. on the screen.

It can have a default image and/or it can have some rendered text.
If both image and text, the text will be rendered on top of the image.

"""
class Gameobject():
    def __init__(self, screen=None, image_folder="", image_file="",
                 center_position=(0,0), font=None, text=""):
        # Check if screen is available
        if screen==None:
            print("Warning: creating gameobject without valid screen")
        else:
            self.screen = screen

        # Create fixed class variables
        self.image = None
        self.image_rect = None
        self.text_image = None
        self.text_rect = None
        self.basic_font = font
        # Load the image
        self.set_image(image_folder, image_file, center_position)
        # Render the text
        self.set_text(self.basic_font, text, center_position)

    def set_image(self, image_folder, image_file, center_position):
        if image_folder != "" and image_file != "":
            # Load image with the input parameters and set the position
            self.image = pygame.image.load(path.join(image_folder, image_file))
            self.image_rect = self.image.get_rect()
            self.image_rect.center = center_position

    def set_text(self, basic_font, text, center_position, color=WHITE):
        if basic_font != None and text != "":
            # Render the text to an image and set the position
            self.text_image = basic_font.render(text, True, color)
            self.text_rect = self.text_image.get_rect()
            self.text_rect.center = center_position

    def draw(self):
        if self.image != None:
            # An image is available, so draw it
            self.screen.blit(self.image, self.image_rect)
        if self.text_image != None:
            # A text image is available, so draw it
            self.screen.blit(self.text_image, self.text_rect)

    def update(self):
        # By default, do nothing
        pass

    def set_center_position(self, position):
        if self.image != None:
            # Set the center of the image
            self.image_rect.center = position
        if self.text_image != None:
            # Set the center of the text image
            self.text_rect.center = position

    def align_new_image_center(self, new_rect):
        # Align another rectangle (e.g. text_rect) on top of the existing image_rect
        new_rect.left = (self.image_rect.width - new_rect.width)/2
        new_rect.top = (self.image_rect.height - new_rect.height)/2
    