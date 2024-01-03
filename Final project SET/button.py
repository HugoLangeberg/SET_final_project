import pygame
from os import path
from settings import *

class Button:
    def __init__(self,coordinates=[0,0,0,0],pressed_color=WHITE,unpressed_color=BLACK,text="",basic_font=""):
        self.coordinates=coordinates
        self.pressed_color=pressed_color
        self.unpressed_color=unpressed_color
        self.is_pressed=False
        self.text=text
        self.basic_font=basic_font

    def draw(self,screen):
        #Draw button on screen.
        rect=pygame.Rect(self.coordinates)
        if self.is_pressed:
            color=self.pressed_color 
        else:
            color=self.unpressed_color
        pygame.draw.rect(screen,color,rect)

        if self.text:
            text_surface=self.font.render(self.text,True,RED)
            text_rect=text_surface.get_rect(center=rect.center)
            screen.blit(text_surface,text_rect)
        
    def check_hover(self):
        x,y=pygame.mouse.get_pos()
        if self.coordinates[0]<x<self.coordinates[0]+self.coordinates[2] and self.coordinates[1]<y<self.coordinates[1]+self.coordinates[3]:
            self.is_pressed=True
        else:
            self.is_pressed=False