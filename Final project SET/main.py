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

deck=Deck()
table=Table()
deck.shuffle()
deck.move_cards(table,12)
print(table)
print(find_sets(table))




