# The next 2 lines of code remove the prompt "Welcome to pygame...." in the terminal
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame

from card import *
from deck import *
from gameobject import *
from os import path
from set import *
from settings import *
from timer import *
from button import *
from table import *

"""
This is the Game class that handles the running of pygame and the gamestates and the logic of the SET game
"""

class Game():
    def __init__(self):
        # Initialize pygame.
        pygame.init()
        # Load additional data, specific for this (SET) game
        self.load_game_data()
        # Set our own SET icon at the top of the window
        pygame.display.set_icon(pygame.image.load(path.join(self.image_folder, FILE_SET_ICON)))
        # Set title at the top of the window
        pygame.display.set_caption(TITLE)
        # Create screen with certain sizes
        self.screen=pygame.display.set_mode((WIDTH, HEIGHT))
        # A clock is needed for a fixed amount of frames-per-second
        self.clock = pygame.time.Clock()
        # The game starts with the start screen
        self.state = STATE_START
        # Assume the game is running now
        self.running = True

    def load_game_data(self):
        # Find the current folder where this game is started
        self.game_folder = path.dirname(__file__)
        # Combine it with the subdirectory for the images
        self.image_folder = path.join(self.game_folder, IMAGE_SUBFOLDER)
        # Fonts are in a separate subfolder
        self.font_folder = path.join(self.game_folder, FONT_SUBFOLDER)
        # Get the fontname
        self.font_name = path.join(self.font_folder, FONT_NAME + '.ttf')
        # Create a font from the TrueType file, size 20
        self.basic_font = pygame.font.Font(self.font_name, 20)
        # Create a timer
        self.timer = Timer()
        # Have an empty string for the selected cards
        self.selected_cards = ""
        # Have an empty string for the currently typed card
        self.card_string = ""
        # The white space between the cards on the screen, needed to determine positions
        self.horizontal_margin = (WIDTH/2-3*CARD_WIDTH)/4
        self.vertical_margin = (HEIGHT-4*CARD_HEIGHT)/5
        # A list with all key positions (center coordinates)
        self.positions = []
        self.create_positions()
        # Initialize player and pc score
        self.player_score = 0
        self.computer_score  = 0

    def load_start_screen(self):
        # Create all objects needed to display on the start screen
        self.background_image = Gameobject(self.screen, self.image_folder, FILE_BACKGROUND,
                                           (WIDTH/2, HEIGHT/2))
        self.watermark_image = Gameobject(self.screen, self.image_folder, FILE_SET_LOGO,
                                          (WIDTH/2, HEIGHT/2))
        self.button1=Button(self.screen, self.image_folder,
                            FILE_BUTTON_START_PRESSED, 
                            FILE_BUTTON_START_UNPRESSED,
                            (WIDTH/2, HEIGHT/4))
        self.button2=Button(self.screen, self.image_folder, 
                            FILE_BUTTON_INSTRUCTIONS_PRESSED,
                            FILE_BUTTON_INSTRUCTIONS_UNPRESSED,
                            (WIDTH/2, HEIGHT/2))
        self.button3=Button(self.screen, self.image_folder, 
                            FILE_BUTTON_QUIT_PRESSED, 
                            FILE_BUTTON_QUIT_UNPRESSED,
                            (WIDTH/2, HEIGHT*3/4))
        # Add all items to the list with gameobjects, which will be updated and drawn every frame
        self.gameobject_list = [self.background_image, self.watermark_image, self.button1, self.button2, self.button3]

    def load_rules_screen(self):
        # Create all objects needed to display on the rules screen with instructions
        self.image = Gameobject(self.screen, self.image_folder, FILE_INSTRUCTIONS, (WIDTH/2, HEIGHT/2))
        # Add this items to the list with gameobjects, so it will be updated and drawn every frame
        self.gameobject_list = [self.image]
            
    def load_game_over_screen(self):
        # game over/continue
        if not self.running:
            return
        # Create the game objects or move existing game objects to correct position
        self.game_over_object = Gameobject(self.screen, "", "", (WIDTH/2, HEIGHT/4), self.basic_font, "GAME OVER")
        self.your_score_object.set_center_position((WIDTH/2, HEIGHT/2))
        self.pc_score_object.set_center_position((WIDTH/2, HEIGHT/2 + 25))
        self.any_key_object = Gameobject(self.screen, "", "", (WIDTH/2, HEIGHT*3/4), self.basic_font, 
                                         "Press a key or click mousebutton to play again")
        self.gameobject_list = [self.background_image, self.game_over_object, self.your_score_object,
                                self.pc_score_object, self.any_key_object]
    
    def load_playing_screen(self):
        # Reset score and time
        self.player_score = 0
        self.computer_score  = 0
        self.level_image = Gameobject(self.screen, "", "", self.positions[TABLE_POSITION_LEVEL],
                                      self.basic_font, "Level Easy - " + str(SEARCH_TIME_EASY) + " seconds")
        # Set the level and start time of the timer
        self.set_level()
        self.timer.counter = self.timer.search_time
        # Create all objects needed to display on the playing screen
        self.background_image = Gameobject(self.screen, self.image_folder, FILE_BACKGROUND, (WIDTH/2, HEIGHT/2))
        self.divider_image = Gameobject(self.screen, self.image_folder, FILE_DIVIDER, (WIDTH/2, HEIGHT/2))
        self.S_image = Gameobject(self.screen, self.image_folder, FILE_S, self.positions[TABLE_POSITION_S])
        self.E_image = Gameobject(self.screen, self.image_folder, FILE_E, self.positions[TABLE_POSITION_E])
        self.T_image = Gameobject(self.screen, self.image_folder, FILE_T, self.positions[TABLE_POSITION_T])
        # Create a table with 12 cards and 12 slot positions (left side of the playing screen)
        self.table=Table(self.screen, self.image_folder, self.basic_font, self.positions)
        # Create a deck with 81 unique cards and shuffle them.
        self.deck=Deck(self.screen, self.image_folder, FILE_DECK, self.positions[TABLE_POSITION_DECK],
                       self.basic_font, str(MAX_NUMBER_OF_CARDS_IN_DECK))
        self.deck.shuffle()
        # Create an empty set that can contain at most 3 cards and knows about the positions on the screen
        self.set=Set(self.screen,"", self.basic_font, self.positions)
        # Get 12 cards from the deck on the table
        for i in range(MAX_NUMBER_OF_CARDS_ON_TABLE):
            # Only get cards if there are still cards left in the deck
            if len(self.deck.cards) > 0:
                self.table.cards.append(self.deck.pop_card())
                # Schedule nice move effect from deck to table position, each card with a slight delay
                self.table.cards[i].move_effects.append((self.positions[TABLE_POSITION_DECK], self.positions[i], FPS/4, i*5))
            else:
                # In case there are no cards, explicitly add None as empty placeholder
                self.table.cards.append(None)

        # Other game objects
        self.your_score_object = Gameobject(self.screen, "", "", self.positions[TABLE_POSITION_YOUR_SCORE],
                                            self.basic_font, "Your score: " + str(self.player_score))
        self.pc_score_object = Gameobject(self.screen, "", "", self.positions[TABLE_POSITION_PC_SCORE],
                                            self.basic_font, "PC score: " + str(self.computer_score))
        self.time_remaining_object = Gameobject(self.screen, "", "", self.positions[TABLE_POSITION_TIME_REMAINING],
                                            self.basic_font, "Time remaining: " + str(self.timer.counter))
        # Add all items to the list with gameobjects, so they will be updated and drawn every frame
        self.gameobject_list=[self.background_image, self.divider_image, self.S_image,
                              self.E_image, self.T_image, self.table, self.deck, self.set,
                              self.your_score_object, self.pc_score_object, self.level_image,
                              self.time_remaining_object]

    def create_positions(self):
        # Create a list with all key center positions on the screen
        # index 0...11 are the 12 card positions
        for i in range(MAX_NUMBER_OF_CARDS_ON_TABLE):
            # Determine center of each card
            x=(i%3+1)*self.horizontal_margin + (i%3+0.5)*CARD_WIDTH
            y=(i//3+1)*self.vertical_margin + (i//3+0.5)*CARD_HEIGHT
            self.positions.append((x,y))
        # index 12 = deck position
        x=6*self.horizontal_margin + 4.5*CARD_WIDTH
        y=self.vertical_margin + 0.5*CARD_HEIGHT
        self.positions.append((x,y))
        # index 13, 14 and 15 are "S" "E" and "T"
        x=5*self.horizontal_margin + 3.5*CARD_WIDTH
        y=2*self.vertical_margin + 1.5*CARD_HEIGHT
        self.positions.append((x,y))
        x=6*self.horizontal_margin + 4.5*CARD_WIDTH
        self.positions.append((x,y))
        x=7*self.horizontal_margin + 5.5*CARD_WIDTH
        self.positions.append((x,y))
        # index 16, 17 and 18 are for selected card1, card2 and card3 in the set
        x=5*self.horizontal_margin + 3.5*CARD_WIDTH
        y=3*self.vertical_margin + 2.5*CARD_HEIGHT
        self.positions.append((x,y))
        x=6*self.horizontal_margin + 4.5*CARD_WIDTH
        self.positions.append((x,y))
        x=7*self.horizontal_margin + 5.5*CARD_WIDTH
        self.positions.append((x,y))
        # index 19, 20 and 21 are for score, pc score, level and time remaining
        x = 6*self.horizontal_margin + 4.5*CARD_WIDTH
        y = 450
        self.positions.append((x,y))
        y = 470
        self.positions.append((x,y))
        y = 510
        self.positions.append((x,y))
        y = 530
        self.positions.append((x,y))

    def events(self):
        # Handle events in the gameloop
        for event in pygame.event.get():
            # Check for a closing window
            if event.type == pygame.QUIT:
                self.running = False
                self.gameloop_running = False
            # Check for mouse presses on the screen.
            elif event.type == pygame.MOUSEBUTTONUP:
                # Check the state of the game (which screen is running) and run appropriate method
                if self.state == STATE_PLAYING:
                    self.event_MB_UP_playing(event)
                elif self.state == STATE_START:
                    self.event_MB_UP_start()
                elif self.state == STATE_RULES or self.state == STATE_GAME_OVER:
                    # To deal with "Press any key or mousebutton to continue"
                    self.event_MB_UP_rules()
            # Our timer will generate an event every second.
            elif event.type == self.timer.timer_event:
                if self.state==STATE_PLAYING:
                    self.event_timer_playing()
            elif event.type == pygame.KEYDOWN:
                if self.state==STATE_PLAYING:
                    # Handle keyboard input
                    self.event_keydown_playing(event)
                elif self.state==STATE_RULES or self.state==STATE_GAME_OVER:
                    # To deal with "Press any key or mousebutton to continue"
                    self.event_MB_UP_rules()

    def event_MB_UP_playing(self, event):
        if self.set.is_valid_set_effect or self.set.is_invalid_set_effect:
            # Ignore mouse clicks during effects
            return
        if self.is_game_over():
            return

        #Check if mouse click is on a card and return that card.
        card_number=self.which_card_is_selected(self.table,event.pos)
        self.move_card_from_table_to_set(card_number)
        # Check if this card movement results in a full set of 3 cards (either valid or invalid)
        self.process_full_set()

    def is_game_over(self):
        if len(self.deck.cards) == 0 and len(self.find_sets(self.table)) == 0 and len(self.set.cards) == 0:
            # No more sets to be found and deck is empty
            self.state = STATE_GAME_OVER
            self.gameloop_running = False
            return True
        return False

    def process_full_set(self):
        if len(self.set.cards) == MAX_NUMBER_OF_CARDS_IN_SET:
            # The set now contains 3 cards
            # If selected_cards string is e.g. "1, 2, 3, ", make it "1, 2, 3"
            self.alternate = self.selected_cards[:-2]
            self.selected_cards= self.alternate
            if self.check_set(self.set.cards[0], self.set.cards[1], self.set.cards[2]):
                # The player created a valid set

                #Remove these cards from the table.
                self.set.valid_set_effect(FPS, FPS/4)
                # Get 3 new cards from the deck (or less if the deck gets empty)
                self.table.replace_cards(self.deck)
                # A point for the player
                self.player_score+=1
                # Adjust score on the screen
                self.your_score_object.set_text(self.basic_font, "Your score: " + str(self.player_score), (520,450))
                # Adjust level if appropriate 
                self.set_level()
                # Set timer according to the level
                self.timer.counter=self.timer.search_time
            else:
                # Player did not select a valid set. Don't remove the cards, but put them back on the table.
                self.set.invalid_set_effect(FPS, FPS/4)
                for i in range(MAX_NUMBER_OF_CARDS_IN_SET):
                    # Restore the 3 cards in the set back on the table
                    self.table.cards[self.set.cards[i].from_position_number] = self.set.cards[i]
                # Empty this invalid set
                self.set.cards.clear()
            self.selected_cards=""
            self.card_string = ""

    def move_card_from_table_to_set(self, card_number):
        if card_number!=-1 and len(self.set.cards) < MAX_NUMBER_OF_CARDS_IN_SET:
            # Valid card 0...11 selected. Add the selected number 1....12 to the string
            self.selected_cards+= str(card_number+1)+ ", "
            # Get card from table and put it in the set
            self.set.cards.append(self.table.pop_card(card_number))
            # Record where this card was on the table
            self.set.cards[-1].from_position_number = card_number
            # And also its position
            self.set.cards[-1].from_position = self.positions[card_number]
            # Start move effect on the last card in the set
            self.set.cards[-1].move_effects.append((self.positions[card_number],
                                           self.positions[TABLE_POSITION_CARD1 + len(self.set.cards) - 1],
                                           FPS/4, 0))

    def event_MB_UP_start(self):
        # Check which button is selected
        if self.button1.hovering:
            # Selected Play button
            self.state = STATE_PLAYING
        elif self.button2.hovering:
            # Selected Instructions button
            self.state = STATE_RULES
        elif self.button3.hovering:
            # Selected to quit the game
            self.running = False
        # Indicate this start screen can stop
        self.gameloop_running = False

    def event_MB_UP_rules(self):
        # A mouse click on this screen means going back to start screen
        self.state = STATE_START
        # Indicate this rules screen with instruction can stop
        self.gameloop_running = False

    def event_timer_playing(self):
        # Another second has passed since the previous timer event
        if len(self.deck.cards) == 0 and len(self.find_sets(self.table)) == 0 and len(self.set.cards) == 0:
            # No more sets to be found, switch to "Game over" state
            self.state = STATE_GAME_OVER
            self.gameloop_running = False
            return
        # If a set was found during the last second, it may be time to switch to a more difficult level
        self.set_level()
        # Decrease the seconds counter
        self.timer.counter -= 1
        # Adjust text on the screen accordingly
        self.time_remaining_object.set_text(self.basic_font, "Time remaining: " + str(self.timer.counter),
                                            self.positions[TABLE_POSITION_TIME_REMAINING])
        # If player has no time left, it's time for the PC
        if self.timer.counter == 0:
            # See if player already selected 1 or 2 cards
            if {len(self.set.cards) > 0 and 
                not self.set.is_invalid_set_effect and
                not self.set.is_valid_set_effect and
                not self.set.is_valid_set_for_pc_effect}:
                # First get the cards from set back to table.
                for i in range(len(self.set.cards)):
                    if self.set.cards[i] != None:
                        card_number = self.set.cards[i].from_position_number
                        self.table.cards[card_number] = self.set.cards[i]
                        # Schedule a nice move effect
                        self.table.cards[card_number].move_effects.append((self.positions[TABLE_POSITION_CARD1+i],
                                                                  self.positions[card_number], 10, 0))
                # Clear the set
                self.set.cards.clear()
            if len(self.table.cards) == MAX_NUMBER_OF_CARDS_ON_TABLE:
                # Find all valid sets on the table
                found_sets=self.find_sets(self.table)
                if found_sets!=[]:
                    # At least 1 valid set was found
                    for i in range(MAX_NUMBER_OF_CARDS_IN_SET):
                        # Get card_number of each card in the first found set
                        card_number = self.table.cards.index(found_sets[0].cards[i])
                        # Get that card from table and put it in the set
                        self.set.cards.append(self.table.pop_card(card_number))
                        # Record where this card was on the table
                        self.set.cards[-1].from_position_number = card_number
                    # Play nice effect to show that computer found a valid set
                    self.set.valid_set_for_pc_effect(FPS, 0)
                    # Adjust score
                    self.computer_score+=1
                    # Set level, if appropriate
                    self.set_level()
                    # Update the score on the screen
                    self.pc_score_object.set_text(self.basic_font, "PC score: " + str(self.computer_score),
                                                  self.positions[TABLE_POSITION_PC_SCORE])
                    # Get new cards from the deck on the table
                    self.table.replace_cards(self.deck)

                else:
                    # No valid sets on the table

                    if self.is_game_over():
                        # It's time to move to game over state
                        return
                    # Create an empty set and move the first 3 cards from the table to that set
                    self.set=Set(self.screen,"", self.basic_font, self.positions)
                    for i in range (MAX_NUMBER_OF_CARDS_IN_SET):
                        self.move_card_from_table_to_set(i)
                    # self.set.invalid_set_effect(FPS/2, 0)
                        # self.set.add_cards([self.table.cards[i]])
                        # self.table.cards[i] = None
                    # Get 3 new cards from the deck on the table
                    self.table.replace_cards(self.deck)
                    self.set.cards.clear()
            # Set timer back to the begin value
            self.timer.counter=self.timer.search_time 
            # Clear the string with selected cards and the single card_string
            self.selected_cards=""
            self.card_string = ""


    def set_level(self):
        # Set the level, depending on the total amount of found sets and update text accordingly
        if self.player_score + self.computer_score >= THRESHOLD_HARD:
            self.timer.search_time = SEARCH_TIME_HARD
            self.level_image.set_text(self.basic_font, "Level Hard - " + str(SEARCH_TIME_HARD) + " seconds",
                                      self.positions[TABLE_POSITION_LEVEL])
        elif self.player_score + self.computer_score >= THRESHOLD_MEDIUM:
            self.timer.search_time = SEARCH_TIME_MEDIUM
            self.level_image.set_text(self.basic_font, "Level Medium - " + str(SEARCH_TIME_MEDIUM) + " seconds",
                                      self.positions[TABLE_POSITION_LEVEL])
        else:
            self.timer.search_time = SEARCH_TIME_EASY
            self.level_image.set_text(self.basic_font, "Level Easy - " + str(SEARCH_TIME_EASY) + " seconds",
                                      self.positions[TABLE_POSITION_LEVEL])


    def event_keydown_playing(self, event):
        # Check for backspace 
        if event.key == pygame.K_BACKSPACE: 
            # get text input from 0 to -1 i.e. end.
            if(self.selected_cards!=""): 
                # Remove last character
                self.selected_cards = self.selected_cards[:-1]
                self.card_string = self.card_string[:-1]
        # Unicode standard is used for string formation 
        elif pygame.K_0 <= event.key <= pygame.K_9:
            # Convert the key code to the corresponding numeric character
            pressed_number = event.key - pygame.K_0
            # Add number to the complete string and to the single cardnumber string
            self.selected_cards += str(pressed_number)
            self.card_string += str(pressed_number)
        elif event.key == pygame.K_SPACE:
            # Add the space
            self.selected_cards+= " "
            # Deal with the finished single card number e.g. "1" or "12"
            self.handle_card_from_keyboard(event)
        elif event.key == pygame.K_COMMA: 
            self.selected_cards+= ","
            # Deal with the finished single card number e.g. "1" or "12"
            self.handle_card_from_keyboard(event)
        elif event.key == pygame.K_RETURN:
            # Deal with the finished single card number e.g. "1" or "12"
            self.handle_card_from_keyboard(event)
            # Reset the strings
            self.selected_cards=""
            self.card_string = ""

    def handle_card_from_keyboard(self, event):
        # If digit(s) are finished, then deal with it. e.g. "1" or "12"
        if self.card_string != "":
            # Convert the string to a cardnumber
            card_number = int(self.card_string)-1
            # Check validity of the number
            if 0 <= card_number < MAX_NUMBER_OF_CARDS_ON_TABLE:
                # Get the position of this card number
                event.pos = self.positions[card_number]
                # Use the position to do as if it was clicked with the mouse
                self.event_MB_UP_playing(event)
            # Reset card string
            self.card_string=""

    def which_card_is_selected(self, table, pos):
        # Return selected card number 0 ... 11 or -1 if not selected anything
        for i in range(len(table.cards)):
            # Go over all cards in the table
            if table.cards[i] != None:
                # If card is still on the table, get its rectangle information
                rect=table.cards[i].image_rect
                # Check if mouse collides with the rectangle
                if rect.collidepoint(pos):
                    # Yes, mouse is on this card
                    return i
        # No card selected
        return -1

    def check_set(self, card1,card2,card3):
        # This method checks if the 3 cards make up a valid set or not

        # Obviously, the cards should be valid cards
        if card1 == None or card2 == None or card3 == None:
            return False
        # Check for each property if either all the cards have the same property or all cards differ.
        if (((card1.color==card2.color and card1.color==card3.color) or (card1.color!=card2.color and card1.color!=card3.color and card2.color!=card3.color)) and
            ((card1.symbol==card2.symbol and card1.symbol==card3.symbol) or (card1.symbol!=card2.symbol and card1.symbol!=card3.symbol and card2.symbol!=card3.symbol)) and
            ((card1.shade==card2.shade and card1.shade==card3.shade) or (card1.shade!=card2.shade and card1.shade!=card3.shade and card2.shade!=card3.shade)) and
            ((card1.number==card2.number and card1.number==card3.number) or (card1.number!=card2.number and card1.number!=card3.number and card2.number!=card3.number))):
            # Valid set!
            return True
        else:
            # Invalid set
            return False
        
    def find_sets(self, table):
        # This method finds all the possible sets on the table.
        # It starts with card 1, 2 and 3, then it checks 1, 2, 4 ... 1, 2, 12.
        # Next, it checks 1, 3, 4 ... 1, 3, 12 and 2, 3, 4 ... 10, 11, 12.
        # Whenever a set it found, it is appended to the list called found_sets.
        found_sets=[]
        for i in range(MAX_NUMBER_OF_CARDS_ON_TABLE-2):
            for j in range(i+1,MAX_NUMBER_OF_CARDS_ON_TABLE-1):
                for k in range(j+1,MAX_NUMBER_OF_CARDS_ON_TABLE):
                    if self.check_set(table.cards[i],table.cards[j],table.cards[k]):
                        set=Set(self.screen,"", self.basic_font, self.positions)
                        set.add_cards([table.cards[i],table.cards[j],table.cards[k]])
                        found_sets.append(set)
        return found_sets

    def check_gamestate(self):
        # Check the gamestate to determine which screen should be loaded
        if self.state == STATE_PLAYING:
            self.load_playing_screen()
        elif self.state == STATE_PAUSE:
            # Not implemented
            pass
        elif self.state == STATE_GAME_OVER:
            self.load_game_over_screen()
        elif self.state == STATE_RULES:
            self.load_rules_screen()
        else:
            # Default situation, e.g. for state STATE_START
            self.load_start_screen()

    # def draw_text(self, surf, txt, color, x, y, align_right = False):
    #     # Draw text on a surface.
    #     text_surface = self.basic_font.render(txt, True, color)  #Render text.
    #     text_rect = text_surface.get_rect()
    #     if align_right:
    #         text_rect.topright=(x, y)
    #     else:
    #         text_rect.midtop = (x, y)
    #     surf.blit(text_surface, text_rect)  #Blit the text.


    def run(self):
        # This is the main game loop that will run as long as the program is running
        while self.running:
            # Check state to load corresponding gameobjects that need to be shown
            self.check_gamestate()
            # (Re)start the gameloop of the screen. It should stop if a state is changed.
            self.gameloop_running = True

            # As long as the current gamestate / screen is active...
            while self.gameloop_running:
                # Ensure equal time for each frame
                self.clock.tick(FPS)
                # Check for events from keyboard, mouse or timer
                self.events()
                # Update and draw all objects on this screen
                for object in self.gameobject_list:
                    # Update game object
                    object.update()
                    # Draw the gameobject
                    object.draw()
                # show the result
                pygame.display.flip()
        # The game has ended. Quit pygame.
        pygame.quit()
