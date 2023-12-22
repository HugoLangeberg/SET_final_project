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


# deck=Deck()
# print(deck)
# Deck.shuffle(deck)
# print(deck)

card1=Card()
card1.shade=2
card2=Card()
card2.shade=1
card3=Card()
card3.shade=2
print(card1,card2,card3)
print(check_set(card1,card2,card3))



