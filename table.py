from card import *
from deck import *
from settings import *
from static_image import *

#We create a class called Table. On the table, there are 12 or more cards.
class Table():
#We define an init method to override the one in the Deck class.
    def __init__(self,deck, screen, image_folder="", font=None):
        self.screen = screen
        self.image_folder = image_folder
        self.font = font
        self.cards=[]
        self.card_is_moving = False
        self.deck = deck
        self.delta_x = 0
        self.delta_y = 0
        self.player_score = 19
        self.computer_score  = 19
        self.counter = 30
        #deck.shuffle()
        #deck.move_cards(self,12)
        self.card_backside_image = pygame.image.load(path.join(self.image_folder, "card_backside.png"))
        self.card_backside_image_rect = self.card_backside_image.get_rect()
        self.horizontal_margin = (WIDTH/2-3*self.card_backside_image_rect.width)/4
        self.vertical_margin = (HEIGHT-4*self.card_backside_image_rect.height)/5
        self.divider_image = static_image(WIDTH/2, HEIGHT/2, self.screen, self.image_folder,
                                  "divider.png")

        self.positions = []
        self.create_positions()

        (x, y) = self.positions[TABLE_POSITION_DECK]
        self.deck_image = static_image(x, y, self.screen, image_folder, "deck.png")
        
        (x,y) = self.positions[TABLE_POSITION_S]
        self.S_image = static_image(x, y, self.screen, image_folder, "S.png")

        (x,y) = self.positions[TABLE_POSITION_E]
        self.E_image = static_image(x, y, self.screen, image_folder, "E.png")

        (x,y) = self.positions[TABLE_POSITION_T]
        self.T_image = static_image(x, y, self.screen, image_folder, "T.png")


    def create_positions(self):
        # index 0...11 are the 12 card positions
        for i in range(MAX_NUMBER_OF_CARDS):
            # Determine center of each card
            x=(i%3+1)*self.horizontal_margin + (i%3+0.5)*self.card_backside_image_rect.width
            y=(i//3+1)*self.vertical_margin + (i//3+0.5)*self.card_backside_image_rect.height
            self.positions.append((x,y))
        # index 12 = deck position
        x=6*self.horizontal_margin + 4.5*self.card_backside_image_rect.width
        y=self.vertical_margin + 0.5*self.card_backside_image_rect.height
        self.positions.append((x,y))

        # index 13, 14 and 15 are "S" "E" and "T"
        x=5*self.horizontal_margin + 3.5*self.card_backside_image_rect.width
        y=2*self.vertical_margin + 1.5*self.card_backside_image_rect.height
        self.positions.append((x,y))
        x=6*self.horizontal_margin + 4.5*self.card_backside_image_rect.width
        self.positions.append((x,y))
        x=7*self.horizontal_margin + 5.5*self.card_backside_image_rect.width
        self.positions.append((x,y))

        # index 16, 17 and 18 are for selected card1, card2 and card3
        x=5*self.horizontal_margin + 3.5*self.card_backside_image_rect.width
        y=3*self.vertical_margin + 2.5*self.card_backside_image_rect.height
        self.positions.append((x,y))
        x=6*self.horizontal_margin + 4.5*self.card_backside_image_rect.width
        self.positions.append((x,y))
        x=7*self.horizontal_margin + 5.5*self.card_backside_image_rect.width
        self.positions.append((x,y))

    #We draw the 12 cards from the table on the screen.
    def draw(self):
        for i in range(len(self.cards)):
            # Set backside image rect accordingly
            self.card_backside_image_rect.center = self.cards[i].image_rect.center
            #self.card_backside_image_rect.centery = self.cards[i].image_rect.centery
            # Blit backside
            self.screen.blit(self.card_backside_image, self.card_backside_image_rect)
            # Do the same for the card front
            self.screen.blit(self.cards[i].image, self.cards[i].image_rect)

            # Determine center of each card position
            (x,y) = (self.cards[i].image_rect.centerx, self.cards[i].image_rect.centery)
            #we draw the numbers 1 to 12 on the screen in certain positions.
            y=y+self.card_backside_image_rect.height/2 + 0
            self.draw_text(self.screen, str(i+1), 20, WHITE, x, y)
        self.divider_image.draw()
        self.deck_image.draw()
        self.S_image.draw()
        self.E_image.draw()
        self.T_image.draw()
        self.draw_text(self.screen, "Your score:", 20, WHITE, 550,450, True)
        self.draw_text(self.screen, str(self.player_score), 20, WHITE, 575,450, True)
        
        self.draw_text(self.screen, "PC score:", 20, WHITE, 550,470, True)
        self.draw_text(self.screen, str(self.computer_score), 20, WHITE, 575,470, True)

        self.draw_text(self.screen, "Time remaining:", 20, WHITE, 550,510, True)
        self.draw_text(self.screen, str(self.counter), 20, WHITE, 575,510, True)

        if self.card_is_moving:
            self.screen.blit(self.moving_card.image, self.moving_card.image_rect)



    def draw_text(self, surf, txt, size, color, x, y, align_right = False):
        # Draw text on a surface.
        text_surface = self.font.render(txt, True, color)  #Render text.
        text_rect = text_surface.get_rect()
        if align_right:
            text_rect.topright=(x, y)
        else:
            text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)  #Blit the text.

    def update(self):
        # Is this the begin of moving a card from deck to left side of the table?
        self.check_move_card_from_deck_to_table()

    def check_move_card_from_deck_to_table(self):
        if len(self.cards) < MAX_NUMBER_OF_CARDS and self.card_is_moving == False:
            self.moving_card = self.deck.pop_card()
            self.moving_card_from_position = self.positions[TABLE_POSITION_DECK]
            self.moving_card_to_position = self.positions[len(self.cards)]
            self.framecount = 0
            self.card_is_moving = True
            self.delta_x = (self.moving_card_to_position[0] - self.moving_card_from_position[0]) / FRAMES_PER_CARD_MOVEMENT
            self.delta_y = (self.moving_card_to_position[1] - self.moving_card_from_position[1]) / FRAMES_PER_CARD_MOVEMENT
            self.moving_card.image_rect.centerx = self.moving_card_from_position[0]
            self.moving_card.image_rect.centery = self.moving_card_from_position[1]

        if self.framecount > 0 and self.card_is_moving:        
            self.moving_card.image_rect.centerx = self.moving_card_from_position[0] + self.framecount*self.delta_x
            self.moving_card.image_rect.centery = self.moving_card_from_position[1] + self.framecount*self.delta_y

        # Is it time to finish the movement of the card?
        if self.framecount == FRAMES_PER_CARD_MOVEMENT:
            if len(self.cards) < MAX_NUMBER_OF_CARDS:
                self.cards.append(self.moving_card)
            self.card_is_moving = False
            self.delta_x = 0
            self.delta_y = 0
            self.framecount = 0

        self.framecount += 1

    #We define a method to replace 3 cards, a given set-object, with cards from the deck.
    def replace_cards(self,deck,set):
        for i in range(len(set.cards)):
            number_card=self.cards.index(set.cards[i])
            self.cards[number_card]=deck.pop_card()
            (self.cards[number_card].image_rect.centerx,self.cards[number_card].image_rect.centery) = self.positions[number_card]
