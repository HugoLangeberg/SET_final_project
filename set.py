from card import *
from gameobject import *
from settings import *

"""
A Set is a gameobject and the Set class inherits from Gameobject
It has no default image or any text

The set contains at most 3 cards. This is not necessarily a valid set.
When cards are not moving, they are visibly located at 3 positions.
"""
class Set(Gameobject):
    def __init__(self,screen, image_folder="", font=None, positions=[]):
        # Initialize first part via the Gameobject
        Gameobject.__init__(self, screen, image_folder,"",(0,0), font, "")
        # Initialize table specific items
        self.positions = positions
        self.cards=[]
        self.is_valid_set_effect = False
        self.is_invalid_set_effect = False
        self.framecount = 0
        self.stop_framecount = -1


    def draw(self):
        # Draw the 3 cards from the set on the screen.
        for i in range(len(self.cards)):
            self.cards[i].draw()
        # Draw the "valid SET!" text, if available
        Gameobject.draw(self)

    def update(self):
        # Update all cards in the set
        for i in range(len(self.cards)):
            self.cards[i].update()

        if self.framecount == self.stop_framecount:
            # It is time to finish the valid_set_effect or invalid_set_effect
            self.is_valid_set_effect = False
            self.is_invalid_set_effect = False
            self.framecount = 0
            self.stop_framecount = -1
            # Remove the text image
            self.text_image = None
            # Clear the set
            self.cards.clear()
        if self.is_valid_set_effect:
            # During this effect, show "Valid set!"
            self.set_text(self.basic_font, "Valid SET found!", self.positions[TABLE_POSITION_CARD2])
            # self.text_rect.top = self.text_rect.top + CARD_HEIGHT/2 + self.text_rect.height/2
            self.framecount += 1
        elif self.is_invalid_set_effect:
            # During this effect, show "Not a valid set!"
            self.set_text(self.basic_font, "Not a valid SET!", self.positions[TABLE_POSITION_CARD2])
            self.framecount += 1

    def valid_set_effect(self, steps):
        # Show the valid set effect during N steps
        self.framecount = 0
        self.stop_framecount = steps
        # Indicate the effect is on
        self.is_valid_set_effect = True
        for i in range(MAX_NUMBER_OF_CARDS_IN_SET):
            self.cards[i].move_effect(self.positions[TABLE_POSITION_CARD1+i], (WIDTH*3/4, HEIGHT+CARD_HEIGHT), 10, 0)

    def invalid_set_effect(self, steps):
        # Show the invalid set effect during N steps
        self.framecount = 0
        self.stop_framecount = steps
        # Indicate the effect is on
        self.is_invalid_set_effect = True
        for i in range(MAX_NUMBER_OF_CARDS_IN_SET):
            self.cards[i].move_effect(self.positions[TABLE_POSITION_CARD1+i], self.cards[i].from_position, 10, 0)

    def pop_card(self):
        # This method removes a card from the set
        return self.cards.pop()
    
    def add_card(self, card):
        # This method adds 1 card to the set.
        self.cards.append(card)

    def add_cards(self, list):
        # Add all cards in the list to this set

        # Ensure the set will not grow beyond 3
        if len(list) + len(self.cards) > 3:
            print("Warning: Attempt to add more cards to the list than possible")
            return
        for i in range(len(list)):
            self.cards.append(list[i])

    def create_set(self, string, table):
        # Create a set of cards, based on the input string
        self.cards=[]
        # User input has a reasonable chance of failing due to user error
        try:
            numbers = string.split(",")
        except ValueError:
            print("This is not a valid format, try again")
            return
        # Ensure that only 3 numbers were given as input
        if len(numbers) != 3:
            print("This is not a valid format, try again")
            return
        # Add these 3 cards to the set
        self.add_cards([table.cards[int(numbers[0])-1], table.cards[int(numbers[1])-1], table.cards[int(numbers[2])-1]])
