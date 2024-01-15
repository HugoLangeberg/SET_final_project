from card import *
from deck import *
from gameobject import *
from settings import *

"""
A Table is a gameobject and the Table class inherits from Gameobject
It has no default image or any text

The table contains at most 12 cards. When cards are not moving, they
are visibly located at the positions 0....

The table also contains 12 position numbers for the 12 slots
"""
class Table(Gameobject):
    def __init__(self,screen, image_folder="", font=None, positions=[]):
        # Initialize first part via the Gameobject
        Gameobject.__init__(self, screen, image_folder,"",(0,0), font, "")
        # Initialize table specific items
        self.positions = positions
        self.cards = []
        self.position_number_images = []
        for i in range(MAX_NUMBER_OF_CARDS_ON_TABLE):
            num = Gameobject(self.screen, "", "", positions[i], self.basic_font, str(i+1))
            # Adjust Y-coordinate of the position number by half a card height
            num.text_rect.top = num.text_rect.top + CARD_HEIGHT/2 + num.text_rect.height/2
            self.position_number_images.append(num)

    def draw(self):
        # Draw the 12 cards from the table on the screen.
        for i in range(len(self.cards)):
            if self.cards[i] != None:
                self.cards[i].draw()
        # Draw the 12 numbers of the positions on the screen
        for item in self.position_number_images:
            item.draw()

    def update(self):
        # Update all cards on the table
        for i in range(len(self.cards)):
            if self.cards[i] != None:
                self.cards[i].update()

    def pop_card(self, index):
        # This method removes a card from the table, based on the index 0...11
        card = self.cards[index]
        card.from_position_number = index
        self.cards[index]=None
        return card
    
    def add_card(self, card):
        # This method adds 1 card to the table.
        self.cards.append(card)

    # This method replaces 3 cards, a given set-object, with cards from the deck.
    def draw_cards_from_deck(self,deck):
        # Counter needed, because each next cards gets a slightly higher delay
        card_sequence = 0
        for i in range(MAX_NUMBER_OF_CARDS_ON_TABLE):
            # Checking all cards positions on the table
            if self.cards[i] == None and len(deck.cards) > 0:
                # Get card from the deck to this table
                self.cards[i]=deck.pop_card()
                # Show a nice move effect
                self.cards[i].move_effects.append((self.positions[TABLE_POSITION_DECK], self.positions[i], FPS/4,
                                                   FPS+card_sequence*5))
                # Update counter for the next card to replace
                card_sequence += 1
