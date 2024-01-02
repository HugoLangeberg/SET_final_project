import pygame
from settings import *

#We create a timer class
class Timer:
    def __init__(self):
        # It has its own eventtype
        self.timer_event = pygame.USEREVENT+1
        # Set the timer for every 1000 milliseconds
        pygame.time.set_timer(self.timer_event, 1000)
        # Time to let the player think (in seconds)
        self.search_time=SEARCH_TIME_EASY
        # Counter does countdown to zero
        self.counter=self.search_time-1

        
        
