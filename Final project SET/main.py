from classes import *


#We define a function which given 3 cards, returns if this is a valid set or not.
def check_set(card1,card2,card3):
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
def find_sets(table):
    found_sets=[]
    amount_of_sets=0
    for i in range(10):
        for j in range(i+1,11):
            for k in range(j+1,12):
                if check_set(table.cards[i],table.cards[j],table.cards[k]):
                    amount_of_sets+=1
                    found_sets.append([str(table.cards[i]),str(table.cards[j]),str(table.cards[k])])
    print(amount_of_sets)
    return found_sets

#We draw the 12 cards from the table on the screen.
def display_cards(table,screen):
    for i in range(len(table.cards)):
        x=50+(i%3)*100
        y=25+(i//3)*125
        screen.blit(table.cards[i].image, (x,y))

def draw_text(surf, txt, size, color, x, y):
    # Draw text on a surface.
    # Font related initialisation.
    font_name = os.path.join(font_folder, 'FreeSans.ttf')  
    font = pygame.font.Font(font_name, size)  #Choose font.
    text_surface = font.render(txt, True, color)  #Render text.
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y) 
    surf.blit(text_surface, text_rect)  #Blit the text.

#we draw the numbers 1 to 12 on the screen in certain positions.
def draw_numbers(table,screen):
    for i in range(len(table.cards)):
        x=80+(i%3)*100
        y=130+(i//3)*125
        draw_text(screen, str(i+1), 20, "red", x, y)


#The function start_game, willinitialize pygame and start the game.
def start_game():
    pygame.init()
    #We create a window with set size.
    screen = pygame.display.set_mode((350,680))
    #We need a clock for fps.
    clock = pygame.time.Clock()   
    #We create a table with 12 cards.
    table=Table()
    #We start running
    print(find_sets(table))
    running = True
    while running:
        #Check for events.
        for event in pygame.event.get():
            #When window is closed, stop running.
            if event.type==pygame.QUIT:
                running=False
        #Fill the screen with a color.
        screen.fill("darkgreen")
        #Render the game here.
        # image=pygame.image.load("greendiamondempty1.gif")
        # card1=Card(0,0,2,2)
        # screen.blit(card1.image, (50,25))
        display_cards(table,screen)
        #We draw the numbers 1 to 12 on the screen, below the cards.
        draw_numbers(table,screen)
        #Show it on the screen.
        pygame.display.flip()
        #Set frames per second.
        clock.tick(60)
    #Quit and clean up pygame and stop running.
    pygame.quit()


start_game()



