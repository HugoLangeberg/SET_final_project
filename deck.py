import pygame
from card import *
from gameobject import *
from os import path
from random import shuffle

"""
A Deck is a gameobject and the Deck class inherits from Gameobject
It has a default image and some text for the amount of cards it
currently contains.

The deck contains at most 81 cards
"""
class Deck(Gameobject):
    def __init__(self, screen=None, image_folder="", image_file="",
                 center_position=(0,0), font=None, text=""):
        # Initialize first part via the Gameobject
        Gameobject.__init__(self, screen, image_folder, image_file, center_position, font, text)
        # Initialize deck specific properties
        self.cards=[]
        # Create 3*3*3*3 = 81 unique cards
        for symbol in range(1):
            for color in range(1):
                for shade in range(3):
                    for number in range(3):
                        card=Card(number,color,symbol,shade, screen, image_folder, center_position)
                        # Append each card to the cards list
                        self.add_card(card)

    def __str__(self):
        # This method prints the names of the cards in the order they are in the deck.
        # Every card is printed on a new line, but it still is just one string.
        stringdeck=[]
        for card in self.cards:
            stringdeck.append(str(card))
        return "\n".join(stringdeck)
    
    def pop_card(self):
        # This method removes a card from the deck.
        return self.cards.pop()
    
    def add_card(self, card):
        # This method adds a card to the deck.
        self.cards.append(card)

    def shuffle(self):
        # This method shuffles the deck.
        shuffle(self.cards)

    def update(self):
        # Show the current number of cards in the deck
        self.set_text(self.basic_font, str(len(self.cards)), self.text_rect.center)

