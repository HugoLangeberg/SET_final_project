import pygame

from card import *
from deck import *
from os import path
from set import *
from settings import *
from timer import *


# This is the Game class that handles the running of pygame
class Game():
    def __init__(self):
        # Initialize pygame.
        pygame.init()
        # Create screen with certain sizes
        self.screen=pygame.display.set_mode((WIDTH, HEIGHT))
        # Set title at the top of the window
        pygame.display.set_caption(TITLE)
        # A clock is needed for a fixed amount of frames-per-second
        self.clock = pygame.time.Clock()
        # Load additional data, specific for this SET game
        self.load_game_data()
        # Assume the game is running now
        self.running = True

    def load_game_data(self):
        self.game_folder = path.dirname(__file__)
        self.cards_folder = path.join(self.game_folder, IMAGE_SUBFOLDER)
        self.font_folder = path.join(self.game_folder, FONT_SUBFOLDER)
        # Get the fontname
        self.font_name = path.join(self.font_folder, FONT_NAME + '.ttf')
        self.basic_font = pygame.font.Font(self.font_name, 20)  #Choose font.

        # Create a timer
        self.timer = Timer()
        self.timer_text = self.basic_font.render(str(self.timer.counter), True, ("white"))

        # Have an empty string for the selected cards
        self.selected_cards = ""
        self.input_text = self.basic_font.render(str(self.selected_cards), True, ("white"))
        self.cards_per_row=3

    
    def new(self):
        # Start a new game
        self.player_score = 0
        self.computer_score  = 0
        #We create a deck with 81 cards.
        self.deck=Deck(self.cards_folder)
        #We create a table with 12 cards.
        self.table=Table(self.deck)
        # We create an emtpy set that can contain 3 cards
        self.set=Set()
        self.run()

    def run(self):
        # Game loop will play 
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
    
    def update(self):
        pass

    def handle_mousebuttondown(self, event):
        #Check if mouse click is on a card and return that card.
        card_number=self.which_card_is_selected(self.table,event.pos)

        if card_number!=-1 and self.table.cards[card_number] not in self.set.cards:    
            self.set.add_card([self.table.cards[card_number]])
            self.selected_cards+= str(self.table.cards.index(self.table.cards[card_number])+1)+ ", "
        if len(self.set.cards)==3:
            #Game.start_game(game)
            self.alternate = self.selected_cards[:-2]
            self.selected_cards= self.alternate
            if self.check_set_string(self.selected_cards, self.table):
                #Remove these cards from the table.
                self.table.replace_cards(self.deck,self.set)
                self.player_score+=1
                self.counter=self.timer.search_time  
                self.set.cards.clear() 
                self.selected_cards=""
            else:
                #Not a set, don't remove the cards.
                pass
            self.set.cards.clear()
            self.selected_cards=""


    def handle_timer(self):
        if(self.timer.counter%5==0):
            print(f"Player score: {self.player_score} Computer score: {self.computer_score}")
            print(f"Deck length: {len(self.deck.cards)} Lengte geselecteerde set: {len(self.set.cards)}")

        self.timer.counter -= 1
        self.timer_text = self.basic_font.render(str(self.timer.counter), True, ("white"))
        if self.timer.counter == 0:
            found_sets=self.find_sets(self.table)
            if found_sets!=[]:
                self.table.replace_cards(self.deck,found_sets[0])
                self.computer_score+=1
            else:
                self.set=Set()
                for i in range (self.cards_per_row):
                    self.set.add_card([self.table.cards[i]])
                self.table.replace_cards(self.deck, self.set)
            self.timer.counter=self.timer.search_time  
            self.set.cards.clear()  
            self.selected_cards=""

    def handle_keydown(self, event):
        # Check for backspace 
        if event.key == pygame.K_BACKSPACE: 
            # get text input from 0 to -1 i.e. end.
            if(self.selected_cards!=""): 
                self.selected_cards = self.selected_cards[:-1] 

        # Unicode standard is used for string 
        # formation 
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
                self.player_score+=1
                self.timer.counter=self.timer.search_time  
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
                if self.playing:
                    self.playing = False
                self.running = False
            #Check for mouse presses on the screen.
            elif event.type==pygame.MOUSEBUTTONDOWN:
                self.handle_mousebuttondown(event)
            #We have a counter that counts.
            elif event.type == self.timer.timer_event:
                self.handle_timer()
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event)
    
    
    def draw(self):
        #Render the game here.
        #Fill the screen with a color.
        self.screen.fill(BG_COLOR)

        self.table.display_cards(self.screen)

        #We draw the numbers 1 to 12 on the screen, below the cards.
        self.draw_numbers(self.table,self.screen)

        input_text = self.basic_font.render(str(self.selected_cards), True, ("white"))
        self.screen.blit(input_text,(150,600))
        self.screen.blit(self.timer_text,(50,600))
                
        #Show it on the screen.
        pygame.display.flip()

    def show_start_screen(self):
        self.screen.fill(BG_COLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Press a key or click mousebutton to play", 16, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pygame.display.flip()
        self.wait_for_key()
    
    def show_game_over_screen(self):
        # game over/continue
        if not self.running:
            return
        self.screen.fill(BG_COLOR)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(self.player_score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key or click mousebutton to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pygame.display.flip()
        self.wait_for_key()
    
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
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
        
    #We define a function which given 3 cards, returns if this is a valid set or not.
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
        for i in range(10):
            for j in range(i+1,11):
                for k in range(j+1,12):
                    if self.check_set(table.cards[i],table.cards[j],table.cards[k]):
                        amount_of_sets+=1
                        set=Set()
                        set.add_card([table.cards[i],table.cards[j],table.cards[k]])
                        found_sets.append(set)
        print(amount_of_sets)
        return found_sets


    def draw_text2(self, surf, txt, size, color, x, y):
        # Draw text on a surface.
        # Font related initialisation.
        font_name = path.join(self.font_folder, 'FreeSans.ttf') 
        font = pygame.font.Font(font_name, 20)  #Choose font.
        
        text_surface = font.render(txt, True, color)  #Render text.
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y) 
        surf.blit(text_surface, text_rect)  #Blit the text.

    #we draw the numbers 1 to 12 on the screen in certain positions.
    def draw_numbers(self, table,screen):
        for i in range(len(table.cards)):
            x=80+(i%3)*100
            y=130+(i//3)*125
            self.draw_text2(screen, str(i+1), 20, "red", x, y)






"""
    #The function start_game, will initialize pygame and start the game.
    def start_game(self):
        
        #We create a timer.
        timer_event = pygame.USEREVENT+1
        pygame.time.set_timer(timer_event, 1000)
        search_time=21
        counter=search_time-1
        text = self.basic_font.render(str(counter), True, ("white"))
        selected_cards = ""
        input_text = self.basic_font.render(str(selected_cards), True, ("white"))

        computer_score=0
        player_score=0
        cards_per_row=3
        #We create a deck with 81 cards.
        deck=Deck()  
        #We create a table with 12 cards.
        table=Table(deck)

        set=Set()
        
        #We start running
        state="start_screen"
        while running:
            #Set frames per second.
            clock.tick(60)
            if state=="start_screen":
                for event in pygame.event.get():
                    if event.type==pygame.MOUSEBUTTONDOWN:
                        state="playing"
                    elif event.type==pygame.QUIT:
                        running=False
            elif state=="playing":
                #Check for events.
                for event in pygame.event.get():
                    #Check for mouse presses on the screen.
                    if event.type==pygame.MOUSEBUTTONDOWN:
                        #Check if mouse click is on a card and return that card.
                        card_number=which_card_is_selected(table,event.pos)

                        if card_number!=-1 and table.cards[card_number] not in set.cards:    
                            set.add_card([table.cards[card_number]])
                            selected_cards+= str(table.cards.index(table.cards[card_number])+1)+ ", "
                        if len(set.cards)==3:
                            Game.start_game(game)
                            alternate = selected_cards[:-2]
                            selected_cards= alternate
                            if check_set_string(selected_cards, table):
                                #Remove these cards from the table.
                                table.replace_cards(deck,set)
                                player_score+=1
                                counter=search_time  
                                set.cards.clear() 
                                selected_cards=""
                            else:
                                #Not a set, don't remove the cards.
                                pass
                            set.cards.clear()
                            selected_cards=""
                            
                    #We have a counter that counts.
                    elif event.type == timer_event:

                        if(counter%5==0):
                            print(f"Player score: {player_score} Computer score: {computer_score}")
                            print(f"Deck length: {len(deck.cards)} Lengte geselecteerde set: {len(set.cards)}")

                        counter -= 1
                        text = self.basic_font.render(str(counter), True, ("white"))
                        if counter == 0:
                            found_sets=find_sets(table)
                            if found_sets!=[]:
                                table.replace_cards(deck,found_sets[0])
                                computer_score+=1
                            else:
                                set=Set()
                                for i in range (cards_per_row):
                                    set.add_card([table.cards[i]])
                                table.replace_cards(deck, set)
                            counter=search_time  
                            set.cards.clear()  
                            selected_cards="" 


                    elif event.type == pygame.KEYDOWN: 
                        # Check for backspace 
                        if event.key == pygame.K_BACKSPACE: 
                            # get text input from 0 to -1 i.e. end.
                            if(selected_cards!=""): 
                                selected_cards = selected_cards[:-1] 
            
                        # Unicode standard is used for string 
                        # formation 
                        elif pygame.K_0 <= event.key <= pygame.K_9:
                            # Convert the key code to the corresponding numeric character
                            pressed_number = event.key - pygame.K_0
                            selected_cards += str(pressed_number)
                        elif event.key == pygame.K_SPACE: 
                        
                                selected_cards+= " "

                        elif event.key == pygame.K_COMMA: 
                            selected_cards+= ","

                        elif event.key == pygame.K_RETURN: 
                            if check_set_string(selected_cards, table):
                                #Remove these cards from the table.
                                set.create_set(selected_cards, table)
                                table.replace_cards(deck,set)
                                player_score+=1
                                counter=search_time  
                                set.cards.clear() 
                                selected_cards=""
                            else:
                                #Not a set, don't remove the cards.
                                pass
                            set.cards.clear()
                            selected_cards=""

                    #When window is closed, stop running.
                    elif event.type==pygame.QUIT:
                        running=False
        
                #Fill the screen with a color.
                self.screen.fill("darkgreen")
                #Render the game here.
                # image=pygame.image.load("greendiamondempty1.gif")
                # card1=Card(0,0,2,2)
                # screen.blit(card1.image, (50,25))
                table.display_cards(self.screen)
                #We draw the numbers 1 to 12 on the screen, below the cards.
                draw_numbers(table,self.screen)

                input_text = self.basic_font.render(str(selected_cards), True, ("white"))
                self.screen.blit(input_text,(150,600))
                self.screen.blit(text,(50,600))
                #Show it on the screen.
                

            pygame.display.flip()
            
        #Quit and clean up pygame and stop running.
        pygame.quit()
"""
