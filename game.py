# The next 2 lines of code remove the prompt "Welcome to pygame...." in the terminal
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame

from card import *
from deck import *
from os import path
from set import *
from settings import *
from timer import *
from button import *
from table import *
from static_image import *


# This is the Game class that handles the running of pygame and the gamestates
class Game():
    def __init__(self):
        # Initialize pygame.
        pygame.init()
        # Load additional data, specific for this (SET) game
        self.load_game_data()
        # Set our own SET icon at the top of the window
        pygame.display.set_icon(pygame.image.load(path.join(self.image_folder, SET_ICON)))
        # Set title at the top of the window
        pygame.display.set_caption(TITLE)
        # Create screen with certain sizes
        self.screen=pygame.display.set_mode((WIDTH, HEIGHT))
        # A clock is needed for a fixed amount of frames-per-second
        self.clock = pygame.time.Clock()
        # The game starts with the start screen
        self.state = "start"
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
        self.cards_per_row = 3
        

        # Load default background image
        self.background_image = pygame.image.load(path.join(self.image_folder,"green_background.png"))

    def load_start_screen(self):
        self.background_image = static_image(WIDTH/2, HEIGHT/2, self.screen,
                                             self.image_folder, "green_background.png")
        self.watermark_image = static_image(WIDTH/2, HEIGHT/2, self.screen,
                                             self.image_folder, "SET_logo.png")
        self.button1=Button((WIDTH/2, HEIGHT/4), self.screen, self.image_folder, 
                            "button_start_pressed.png", 
                            "button_start_unpressed.png")
        self.button2=Button((WIDTH/2, HEIGHT/2), self.screen, self.image_folder, 
                            "button_instructions_pressed.png", 
                            "button_instructions_unpressed.png")
        self.button3=Button((WIDTH/2, HEIGHT*3/4), self.screen, self.image_folder, 
                            "button_quit_pressed.png", 
                            "button_quit_unpressed.png")
        self.gameobject_list = [self.background_image, self.watermark_image, self.button1, self.button2, self.button3]

    def load_rules_screen(self):
        self.image = static_image(WIDTH/2, HEIGHT/2, self.screen,
                                             self.image_folder, "instructions.png")
        self.gameobject_list = [self.image]
            
    def load_playing_screen(self):
        # Start a new game

        #We create a deck with 81 cards.
        self.deck=Deck((500,75),self.screen, self.image_folder, "deck.png")
        #We create a table with 12 cards.
        self.table=Table(self.deck, self.screen, self.image_folder, self.basic_font)
        self.table.timer_text = self.basic_font.render(str(30), True, WHITE)
        # We create an emtpy set that can contain 3 cards
        self.set=Set()
        self.background_image = static_image(WIDTH/2, HEIGHT/2, self.screen,
                                             self.image_folder, "green_background.png")
        # card = self.deck.pop_card()
        # card.move_effect(card.image_rect.center, (0,0), FPS)
        # card2 = self.deck.pop_card()
        # card2.set_center_position((WIDTH/2, HEIGHT/2))
        # card2.move_effect((WIDTH/2, HEIGHT/2), (WIDTH,0), FPS)

        
        
        self.gameobject_list=[self.background_image, self.table, self.deck]
    
    def update(self):
        pass

    def handle_mousebuttondown(self, event):
        #Check if mouse click is on a card and return that card.
        card_number=self.which_card_is_selected(self.table,event.pos)

        if card_number!=-1 and self.table.cards[card_number] not in self.set.cards:    
            self.set.add_card([self.table.cards[card_number]])
            (self.table.cards[card_number].image_rect.centerx,self.table.cards[card_number].image_rect.centery)=\
                self.table.positions[TABLE_POSITION_CARD1+len(self.set.cards)-1]
            self.selected_cards+= str(self.table.cards.index(self.table.cards[card_number])+1)+ ", "
        if len(self.set.cards)==3:
            #Game.start_game(game)
            self.alternate = self.selected_cards[:-2]
            self.selected_cards= self.alternate
            if self.check_set_string(self.selected_cards, self.table):
                #Remove these cards from the table.
                self.table.replace_cards(self.deck,self.set)
                self.table.player_score+=1
                self.timer.counter=self.timer.search_time
                self.table.counter = self.timer.counter
                self.set.cards.clear() 
                self.selected_cards=""
            else:
                #Not a set, don't remove the cards.
                pass
            self.set.cards.clear()
            self.selected_cards=""


    def handle_timer(self):
        if(self.timer.counter%5==0):
            print(f"Player score: {self.table.player_score} Computer score: {self.table.computer_score}")
            #print(f"Deck length: {len(self.deck.cards)} Lengte geselecteerde set: {len(self.set.cards)}")

        self.timer.counter -= 1
        self.table.counter = self.timer.counter
        #self.table.timer_text = self.basic_font.render(str(self.timer.counter), True, ("white"))
        if self.timer.counter == 0:
            if len(self.table.cards) == MAX_NUMBER_OF_CARDS:
                found_sets=self.find_sets(self.table)
                if found_sets!=[]:
                    self.table.replace_cards(self.deck,found_sets[0])
                    self.table.computer_score+=1
                else:
                    self.set=Set()
                    for i in range (self.cards_per_row):
                        self.set.add_card([self.table.cards[i]])
                    self.table.replace_cards(self.deck, self.set)
            self.timer.counter=self.timer.search_time 
            self.table.counter = self.timer.counter

            self.set.cards.clear()  
            self.selected_cards=""

    def handle_keydown(self, event):
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
                self.table.replace_cards(self.deck,self.set)
                self.table.player_score+=1
                self.timer.counter=self.timer.search_time  
                self.table.counter = self.timer.counter
                self.set.cards.clear() 
                self.selected_cards=""
            else:
                #Not a set, don't remove the cards.
                pass
            self.set.cards.clear()
            self.selected_cards=""

    def events(self):
        # Handle events in the gameloop
        for event in pygame.event.get():
            # Check for a closing window
            if event.type == pygame.QUIT:
                self.running = False
                self.gameloop_running = False
                
            #Check for mouse presses on the screen.
            elif event.type==pygame.MOUSEBUTTONUP:
                if self.state=="playing":
                    self.handle_mousebuttondown(event)
                elif self.state =="start":
                    self.events_start()
                elif self.state =="rules":
                    self.events_rules()
                     
            #We have a counter that counts.
            elif event.type == self.timer.timer_event:
                if self.state=="playing":
                    self.handle_timer()
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event)

    def events_start(self):
        if self.button1.hovered:
           self.state = "playing"
        elif self.button2.hovered:
            self.state = "rules"
        elif self.button3.hovered:
            self.running = False
        self.gameloop_running = False

    def events_rules(self):
        self.state = "start"
        self.gameloop_running = False

    def load_game_over_screen(self):
        # game over/continue
        if not self.running:
            return
        self.screen.fill(BG_COLOR)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(self.table.player_score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key or click mousebutton to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pygame.display.flip()
        self.wait_for_key()
    
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                self.button.check_is_pressed(event)
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if (event.type == pygame.KEYUP) or (event.type == pygame.MOUSEBUTTONDOWN):
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def which_card_is_selected(self, table, pos):
        for i in range(len(table.cards)):
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
        for i in range(MAX_NUMBER_OF_CARDS-2):
            for j in range(i+1,MAX_NUMBER_OF_CARDS-1):
                for k in range(j+1,MAX_NUMBER_OF_CARDS):
                    if self.check_set(table.cards[i],table.cards[j],table.cards[k]):
                        amount_of_sets+=1
                        set=Set()
                        set.add_card([table.cards[i],table.cards[j],table.cards[k]])
                        found_sets.append(set)
        print(amount_of_sets)
        return found_sets

    # As long as the program is active
    def check_gamestate(self):
        if self.state == "playing":
            self.load_playing_screen()
        elif self.state == "pause":
            self.load_pause_screen()
        elif self.state == "game_over":
            self.load_game_over_screen()
        elif self.state == "rules":
            self.load_rules_screen()
        else:
            # Default situation, e.g. for state "start"
            self.load_start_screen()

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
