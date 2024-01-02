from game import *

game = Game()
game.show_start_screen()
while game.running:
    game.new()
    game.show_game_over_screen()

pygame.quit()



