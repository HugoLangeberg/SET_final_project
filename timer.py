import pygame
from settings import *

"""
A Timer is a class to measure the time.
The timer will give a user defined event every 1000 msec (=1 Sec)
It has no default image or any text.

The counter will start at a specific search time and will do
a countdown to 0

The table contains at most 12 cards. When cards are not moving, they
are visibly located at the positions 0....11
"""
class Timer:
    def __init__(self):
        # It has its own eventtype
        self.timer_event = pygame.USEREVENT+1
        # Set the timer for every 1000 milliseconds
        pygame.time.set_timer(self.timer_event, 1000)
        # Time to let the player think (in seconds)
        self.search_time=SEARCH_TIME_EASY+1
        # Counter does countdown to zero
        self.counter=self.search_time       
        
