import pygame

from os import path

class static_image():
    def __init__(self, center_x=0, center_y=0, screen=None, image_folder="", image_filename=""):
        self.screen = screen
        self.image=pygame.image.load(path.join(image_folder, image_filename))
        self.image_rect = self.image.get_rect()
        self.image_rect.center=(center_x, center_y)

    def update(self):
        pass

    def draw(self):
        self.screen.blit(self.image, self.image_rect)
