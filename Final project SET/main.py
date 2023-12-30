from classes import *

#We define a function which given 3 cards, returns if this is a valid set or not.
def check_set_string(input_string, table):
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

    return check_set(card1, card2, card3)
    
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
                    set=Set()
                    set.add_card([table.cards[i],table.cards[j],table.cards[k]])
                    found_sets.append(set)
    print(amount_of_sets)
    return found_sets

def draw_text(surf, txt, size, color, x, y):
    # Draw text on a surface.
    # Font related initialisation.
    font_name = os.path.join(font_folder, 'FreeSans.ttf') 
    font = pygame.font.Font(font_name, 20)  #Choose font.
    
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

def which_card_is_selected(table,pos):
    for i in range(len(table.cards)):
        rect=table.cards[i].image_rect
        if rect.collidepoint(pos):
            return i
    return -1

#The function start_game, will initialize pygame and start the game.
def start_game():
    pygame.init()
    #We create a window with set size.
    screen = pygame.display.set_mode((350,680))
    font_name = os.path.join(font_folder, 'FreeSans.ttf')  
    basic_font = pygame.font.Font(font_name, 20)  #Choose font.
    #We need a clock for fps.
    clock = pygame.time.Clock() 
    #We create a timer.
    timer_event = pygame.USEREVENT+1
    pygame.time.set_timer(timer_event, 1000)
    search_time=21
    counter=search_time-1
    text = basic_font.render(str(counter), True, ("white"))
    selected_cards = ""
    input_text = basic_font.render(str(selected_cards), True, ("white"))

    computer_score=0
    player_score=0
    cards_per_row=3
    #We create a deck with 81 cards.
    deck=Deck()  
    #We create a table with 12 cards.
    table=Table(deck)

    set=Set()
    #We start running
    running = True
    while running:
        #Set frames per second.
        clock.tick(60)
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
                text = basic_font.render(str(counter), True, ("white"))
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
        screen.fill("darkgreen")
        #Render the game here.
        # image=pygame.image.load("greendiamondempty1.gif")
        # card1=Card(0,0,2,2)
        # screen.blit(card1.image, (50,25))
        table.display_cards(screen)
        #We draw the numbers 1 to 12 on the screen, below the cards.
        draw_numbers(table,screen)

        input_text = basic_font.render(str(selected_cards), True, ("white"))
        screen.blit(input_text,(150,600))
        screen.blit(text,(50,600))
        #Show it on the screen.
        

        pygame.display.flip()
        
    #Quit and clean up pygame and stop running.
    pygame.quit()


start_game()



