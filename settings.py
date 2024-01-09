# Game options/settings
TITLE                               = "SET"
WIDTH                               = 700
HEIGHT                              = 560
FPS                                 = 60
FRAMES_PER_CARD_MOVEMENT            = FPS/10
FONT_NAME                           = "FreeSans"
FONT_SUBFOLDER                      = "font"
IMAGE_SUBFOLDER                     = "images"
BG_COLOR                            = "darkgreen"
MAX_NUMBER_OF_CARDS_ON_TABLE        = 12 
MAX_NUMBER_OF_CARDS_IN_SET          = 3
MAX_NUMBER_OF_CARDS_IN_DECK         = 9
CARD_WIDTH                          = 70  # px
CARD_HEIGHT                         = 110 # px

# Number of seconds to let player search for a set
SEARCH_TIME_EASY                    = 5     # Temporary for testing, otherwise 30
SEARCH_TIME_MEDIUM                  = 20
SEARCH_TIME_HARD                    = 15

# define colors as (RED, GREEN, BLUE) tuples
WHITE                               = (255, 255, 255)
BLACK                               = (0, 0, 0)

# Selfmade image files
FILE_BACKGROUND                     = "green_background.png"
FILE_BUTTON_START_UNPRESSED         = "button_start_unpressed.png"
FILE_BUTTON_START_PRESSED           = "button_start_pressed.png"
FILE_BUTTON_INSTRUCTIONS_UNPRESSED  = "button_instructions_unpressed.png"
FILE_BUTTON_INSTRUCTIONS_PRESSED    = "button_instructions_pressed.png"
FILE_BUTTON_QUIT_UNPRESSED          = "button_quit_unpressed.png"
FILE_BUTTON_QUIT_PRESSED            = "button_quit_pressed.png"
FILE_CARD_BACKSIDE                  = "card_backside.png"
FILE_DECK                           = "deck.png"
FILE_DIVIDER                        = "divider.png"
FILE_INSTRUCTIONS                   = "instructions.png"
FILE_SET_ICON                       = "SET_icon32.png"
FILE_SET_LOGO                       = "SET_logo.png"
FILE_S                              = "S.png"
FILE_E                              = "E.png"
FILE_T                              = "T.png"

# define positions on the screen
TABLE_POSITION_1                    = 0 # The positions where 12 cards should be drawn
TABLE_POSITION_2                    = 1
TABLE_POSITION_3                    = 2
TABLE_POSITION_4                    = 3
TABLE_POSITION_5                    = 4
TABLE_POSITION_6                    = 5
TABLE_POSITION_7                    = 6
TABLE_POSITION_8                    = 7
TABLE_POSITION_9                    = 8
TABLE_POSITION_10                   = 9
TABLE_POSITION_11                   = 10
TABLE_POSITION_12                   = 11
TABLE_POSITION_DECK                 = 12 # Where the deck should be drawn
TABLE_POSITION_S                    = 13 # 'S'
TABLE_POSITION_E                    = 14 # 'E'
TABLE_POSITION_T                    = 15 # 'T'
TABLE_POSITION_CARD1                = 16 # 1st selected card
TABLE_POSITION_CARD2                = 17 # 2nd selected card
TABLE_POSITION_CARD3                = 18 # 3th selected 
TABLE_POSITION_YOUR_SCORE           = 19
TABLE_POSITION_PC_SCORE             = 20
TABLE_POSITION_TIME_REMAINING       = 21

# Game states
STATE_START                         = "start"
STATE_PLAYING                       = "playing"
STATE_PAUSE                         = "pause"
STATE_GAME_OVER                     = "game_over"
STATE_RULES                         = "rules"
