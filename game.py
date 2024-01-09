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
        # The white space between the cards on the screen, needed to determine positions
        self.horizontal_margin = (WIDTH/2-3*CARD_WIDTH)/4
        self.vertical_margin = (HEIGHT-4*CARD_HEIGHT)/5
        # A list with all key positions (center coordinates)
        self.positions = []
        self.create_positions()
        self.player_score = 19
        self.computer_score  = 19
        # Starting time (seconds)
        self.counter = SEARCH_TIME_EASY

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
        self.gameobject_list.clear()
        self.game_over_object = Gameobject(self.screen, "", "", (WIDTH/2, HEIGHT/4), self.basic_font, "GAME OVER")
        # self.your_score_object = Gameobject(self.screen, "", "", self.positions[TABLE_POSITION_YOUR_SCORE],
        #                                     self.basic_font, "Your score: " + str(self.player_score))
        self.your_score_object.set_center_position((WIDTH/2, HEIGHT/2))
        # self.pc_score_object = Gameobject(self.screen, "", "", self.positions[TABLE_POSITION_PC_SCORE],
        #                                     self.basic_font, "PC score: " + str(self.computer_score))
        self.pc_score_object.set_center_position((WIDTH/2, HEIGHT/2 + 25))
        self.any_key_object = Gameobject(self.screen, "", "", (WIDTH/2, HEIGHT*3/4), self.basic_font, 
                                         "Press a key or click mousebutton to play again")
        self.gameobject_list = [self.background_image, self.game_over_object, self.your_score_object,
                                self.pc_score_object, self.any_key_object]
        # self.draw_text(self.screen, "GAME OVER", WHITE, WIDTH / 2, HEIGHT / 4)
        # self.draw_text(self.screen, "Your Score: " + str(self.player_score), WHITE, WIDTH / 2, HEIGHT / 2)
        # self.draw_text(self.screen, "PC Score: " + str(self.computer_score), WHITE, WIDTH / 2, HEIGHT / 2+25)
        # self.draw_text(self.screen, "Press a key or click mousebutton to play again", WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        # pygame.display.flip()
        # self.wait_for_key()
    
    def load_playing_screen(self):
        # Create all objects needed to display on the playing screen
        self.background_image = Gameobject(self.screen, self.image_folder, FILE_BACKGROUND, (WIDTH/2, HEIGHT/2))
        self.divider_image = Gameobject(self.screen, self.image_folder, FILE_DIVIDER, (WIDTH/2, HEIGHT/2))
        self.S_image = Gameobject(self.screen, self.image_folder, FILE_S, self.positions[TABLE_POSITION_S])
        self.E_image = Gameobject(self.screen, self.image_folder, FILE_E, self.positions[TABLE_POSITION_E])
        self.T_image = Gameobject(self.screen, self.image_folder, FILE_T, self.positions[TABLE_POSITION_T])
        # Create a table with 12 cards and 12 slot positions (left side of the playing screen)
        self.table=Table(self.screen, self.image_folder, self.basic_font, self.positions)
        # Create a deck with 81 unique cards.
        self.deck=Deck(self.screen, self.image_folder, FILE_DECK, self.positions[TABLE_POSITION_DECK],
                       self.basic_font, str(MAX_NUMBER_OF_CARDS_IN_DECK))
        # Create an empty set that can contain at most 3 cards
        self.set=Set(self.screen,"", self.basic_font, self.positions)
        # Get 12 cards from the deck on the table
        for i in range(MAX_NUMBER_OF_CARDS_ON_TABLE):
            if len(self.deck.cards) > 0:
                self.table.cards.append(self.deck.pop_card())
                self.table.cards[i].move_effect(self.positions[TABLE_POSITION_DECK], self.positions[i], FPS/4, i*5)
            else:
                self.table.cards.append(None)

        self.your_score_object = Gameobject(self.screen, "", "", self.positions[TABLE_POSITION_YOUR_SCORE],
                                            self.basic_font, "Your score: " + str(self.player_score))
        self.pc_score_object = Gameobject(self.screen, "", "", self.positions[TABLE_POSITION_PC_SCORE],
                                            self.basic_font, "PC score: " + str(self.computer_score))
        self.time_remaining_object = Gameobject(self.screen, "", "", self.positions[TABLE_POSITION_TIME_REMAINING],
                                            self.basic_font, "Time remaining: " + str(self.counter))
        # Add all items to the list with gameobjects, so they will be updated and drawn every frame
        self.gameobject_list=[self.background_image, self.divider_image, self.S_image,
                              self.E_image, self.T_image, self.table, self.deck, self.set,
                              self.your_score_object, self.pc_score_object, self.time_remaining_object]

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
        # index 19, 20 and 21 are for score, pc score and time remaining
        x = 6*self.horizontal_margin + 4.5*CARD_WIDTH
        y = 450
        self.positions.append((x,y))
        y = 470
        self.positions.append((x,y))
        y = 510
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
                # Check the state of the game (which screen is running)
                if self.state == STATE_PLAYING:
                    self.event_MB_UP_playing(event)
                elif self.state == STATE_START:
                    self.event_MB_UP_start()
                elif self.state == STATE_RULES:
                    self.event_MB_UP_rules()
                elif self.state == STATE_GAME_OVER:
                    self.event_MB_UP_rules()
            # A timer will generate an event every second.
            elif event.type == self.timer.timer_event:
                if self.state==STATE_PLAYING:
                    self.event_timer_playing()
            elif event.type == pygame.KEYDOWN:
                if self.state==STATE_PLAYING:
                    self.event_keydown_playing(event)
                elif self.state==STATE_RULES or self.state==STATE_GAME_OVER:
                    # Press any key or mousebutton to continue
                    self.event_MB_UP_rules()

    def event_MB_UP_playing(self, event):
        if self.set.is_valid_set_effect or self.set.is_invalid_set_effect:
            # Ignore mouse clicks during effects
            return
        if len(self.deck.cards) == 0 and len(self.find_sets(self.table)) == 0 and len(self.set.cards) == 0:
            # No more sets to be found
            self.state = STATE_GAME_OVER
            self.gameloop_running = False
            return

        #Check if mouse click is on a card and return that card.
        card_number=self.which_card_is_selected(self.table,event.pos)

            
        if card_number!=-1 and len(self.set.cards) < MAX_NUMBER_OF_CARDS_IN_SET:
            # Valid card 0...11 selected. Add the selected number 1....12 to the string
            self.selected_cards+= str(card_number+1)+ ", "
            # Get card from table and put it in the set
            self.set.cards.append(self.table.pop_card(card_number))
            # Record where this card was on the table
            self.set.cards[-1].from_position_number = card_number
            # Start move effect on the last card in the set
            self.set.cards[-1].move_effect(self.positions[card_number],
                                           self.positions[TABLE_POSITION_CARD1 + len(self.set.cards) - 1],
                                           FPS/4, 0)
        if len(self.set.cards) == MAX_NUMBER_OF_CARDS_IN_SET:
            # The set now contains 3 cards
            self.alternate = self.selected_cards[:-2]
            self.selected_cards= self.alternate
            if self.check_set(self.set.cards[0], self.set.cards[1], self.set.cards[2]):
            # if self.check_set_string(self.selected_cards, self.set):
                #Remove these cards from the table.
                self.set.valid_set_effect(FPS)
                self.table.replace_cards(self.deck)
                self.player_score+=1
                self.your_score_object.set_text(self.basic_font, "Your score: " + str(self.player_score), (520,450))
                self.timer.counter=self.timer.search_time
            else:
                #Not a set, don't remove the cards, but put them back on the table.
                self.set.invalid_set_effect(FPS)
                for i in range(MAX_NUMBER_OF_CARDS_IN_SET):
                    # Restore the 3 cards in the set back to their original place on the table
                    self.table.cards[self.set.cards[i].from_position_number] = self.set.cards[i]
                # Empty this set
                self.set.cards.clear()
            # self.set.cards.clear()
            self.selected_cards=""

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
        if len(self.deck.cards) == 0 and len(self.find_sets(self.table)) == 0 and len(self.set.cards) == 0:
            # No more sets to be found
            self.state = STATE_GAME_OVER
            self.gameloop_running = False
            return

        self.timer.counter -= 1
        self.time_remaining_object.set_text(self.basic_font, "Time remaining: " + str(self.timer.counter),
                                            self.positions[TABLE_POSITION_TIME_REMAINING])
        if self.timer.counter == 0:
            if len(self.table.cards) == MAX_NUMBER_OF_CARDS_ON_TABLE:
                found_sets=self.find_sets(self.table)
                if found_sets!=[]:
                    # self.table.replace_cards(self.deck,found_sets[0])
                    self.table.replace_cards(self.deck)
                    # Reset the local set, because PC will use it.
                    self.set.cards.clear()
                    for i in range(MAX_NUMBER_OF_CARDS_IN_SET):
                        card_number = self.table.cards.index(found_sets[0].cards[i])
                        # Get card from table and put it in the set
                        self.set.cards.append(self.table.pop_card(card_number))
                        # Record where this card was on the table
                        self.set.cards[-1].from_position_number = card_number
                        # Start move effect on the last card in the set
                        self.set.cards[-1].move_effect(self.positions[card_number],
                                                    self.positions[TABLE_POSITION_CARD1 + len(self.set.cards) - 1],
                                                    FPS/4, 0)
            
                    self.computer_score+=1
                    self.pc_score_object.set_text(self.basic_font, "PC score: " + str(self.computer_score),
                                                  self.positions[TABLE_POSITION_PC_SCORE])
                else:
                    self.set=Set(self.screen,"", self.basic_font, self.positions)
                    for i in range (MAX_NUMBER_OF_CARDS_IN_SET):
                        self.set.add_cards([self.table.cards[i]])
                    self.table.replace_cards(self.deck)
            self.timer.counter=self.timer.search_time 

            # self.set.cards.clear()  
            self.selected_cards=""

    def event_keydown_playing(self, event):
        # Check for backspace 
        if event.key == pygame.K_BACKSPACE: 
            # get text input from 0 to -1 i.e. end.
            if(self.selected_cards!=""): 
                self.selected_cards = self.selected_cards[:-1] 

        # Unicode standard is used for string formation 
        elif pygame.K_0 <= event.key <= pygame.K_9:
            # Convert the key code to the corresponding numeric character
            pressed_number = event.key - pygame.K_0
            self.selected_cards += str(pressed_number)
        elif event.key == pygame.K_SPACE: 
                self.selected_cards+= " "
        elif event.key == pygame.K_COMMA: 
            self.selected_cards+= ","
        elif event.key == pygame.K_RETURN: 
            if self.check_set_string(self.selected_cards, self.table):
                #Remove these cards from the table.
                self.set.create_set(self.selected_cards, self.table)
                self.table.replace_cards(self.deck)
                self.player_score+=1
                self.your_score_object.set_text(self.basic_font, "Your score: " + str(self.player_score), (520,450))
                self.timer.counter=self.timer.search_time  
                self.set.cards.clear() 
                self.selected_cards=""
            else:
                #Not a set, don't remove the cards.
                pass
            self.set.cards.clear()
            self.selected_cards=""

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                # self.button.check_is_pressed(event)
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if (event.type == pygame.KEYUP) or (event.type == pygame.MOUSEBUTTONDOWN):
                    waiting = False

    # def draw_text(self, text, size, color, x, y):
    #     font = pygame.font.Font(self.font_name, size)
    #     text_surface = font.render(text, True, color)
    #     text_rect = text_surface.get_rect()
    #     text_rect.midtop = (x, y)
    #     self.screen.blit(text_surface, text_rect)

    def which_card_is_selected(self, table, pos):
        # Return selected card number 0 ... 11 or -1 if not selected anything
        for i in range(len(table.cards)):
            if table.cards[i] != None:
                rect=table.cards[i].image_rect
                if rect.collidepoint(pos):
                    return i
        return -1

    #We define a function which given 3 cards, returns if this is a valid set or not.
    def check_set_string(self, input_string, table):
        try:
            numbers = input_string.split(",")
        except ValueError:
            print("This is not a valid format, try again")
            return
        
        if len(numbers) != 3:
            print("This is not a valid format, try again")
            return
        
        card1 = table.cards[int(numbers[0])-1]
        card2 = table.cards[int(numbers[1])-1]
        card3 = table.cards[int(numbers[2])-1]

        return self.check_set(card1, card2, card3)
        
    #We define a function which evaluated the input of 3 cards and returns if this is a valid set (True) or not (False).
    def check_set(self, card1,card2,card3):
        #We write an if-statement to check for each property if either all the cards have the same property or all cards differ.
        if card1 == None or card2 == None or card3 == None:
            return False
        if (((card1.color==card2.color and card1.color==card3.color) or (card1.color!=card2.color and card1.color!=card3.color and card2.color!=card3.color)) and
            ((card1.symbol==card2.symbol and card1.symbol==card3.symbol) or (card1.symbol!=card2.symbol and card1.symbol!=card3.symbol and card2.symbol!=card3.symbol)) and
            ((card1.shade==card2.shade and card1.shade==card3.shade) or (card1.shade!=card2.shade and card1.shade!=card3.shade and card2.shade!=card3.shade)) and
            ((card1.number==card2.number and card1.number==card3.number) or (card1.number!=card2.number and card1.number!=card3.number and card2.number!=card3.number))):
            return True
        else:
            return False
        
    #We define a function which finds all the possible sets on the table.
    #The amount of set for temporary convenience.
    #We start with card 1, 2 and 3, then we check 1, 2, 4 ... 1, 2, 12.
    #Then we check 1, 3, 4 ... 1, 3, 12 and 2, 3, 4 ... 10, 11, 12.
    #Whenever we find a set, we append this set to the list called found_sets.
    def find_sets(self, table):
        found_sets=[]
        amount_of_sets=0
        for i in range(MAX_NUMBER_OF_CARDS_ON_TABLE-2):
            for j in range(i+1,MAX_NUMBER_OF_CARDS_ON_TABLE-1):
                for k in range(j+1,MAX_NUMBER_OF_CARDS_ON_TABLE):
                    if self.check_set(table.cards[i],table.cards[j],table.cards[k]):
                        amount_of_sets+=1
                        set=Set(self.screen,"", self.basic_font, self.positions)
                        set.add_cards([table.cards[i],table.cards[j],table.cards[k]])
                        found_sets.append(set)
        return found_sets

    # As long as the program is active
    def check_gamestate(self):
        if self.state == STATE_PLAYING:
            self.load_playing_screen()
        elif self.state == STATE_PAUSE:
            self.load_pause_screen()
        elif self.state == STATE_GAME_OVER:
            self.load_game_over_screen()
        elif self.state == STATE_RULES:
            self.load_rules_screen()
        else:
            # Default situation, e.g. for state STATE_START
            self.load_start_screen()

    def draw_text(self, surf, txt, color, x, y, align_right = False):
        # Draw text on a surface.
        text_surface = self.basic_font.render(txt, True, color)  #Render text.
        text_rect = text_surface.get_rect()
        if align_right:
            text_rect.topright=(x, y)
        else:
            text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)  #Blit the text.


    def run(self):
        while self.running:
            # Check state to load corresponding gameobjects that need to be shown
            self.check_gamestate()
            # (Re)start the gameloop. It should stop if a state is changed.
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
