import pygame
from os import path
from settings import *

class Button:
    def __init__(self,center_coordinates=(0,0),screen=None,image_folder="", pressed_image="",unpressed_image=""):
        self.pressed_image=pygame.image.load(path.join(image_folder, pressed_image))
        self.pressed_imagerect = self.pressed_image.get_rect()
        self.pressed_imagerect.center = center_coordinates
        self.unpressed_image=pygame.image.load(path.join(image_folder, unpressed_image))
        self.unpressed_imagerect = self.unpressed_image.get_rect()
        self.unpressed_imagerect.center = center_coordinates
        self.hovered=False
        self.screen = screen

    def draw(self):
        #Draw pressed or unpressed button on screen (depending where mouse is hovering)
        if self.hovered:
            # Mouse is above the button
            self.screen.blit(self.pressed_image, self.pressed_imagerect)
        else:
            # Mouse is not above the button
            self.screen.blit(self.unpressed_image, self.unpressed_imagerect)

    def check_hover(self):
        x,y=pygame.mouse.get_pos()
        if self.pressed_imagerect.collidepoint(x,y):
            self.hovered=True
        else:
            self.hovered=False

    def update(self):
        # During update, check if the mouse is above the button or not
        self.check_hover()