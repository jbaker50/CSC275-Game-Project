#defining game variables

#basic map rn, just to test collision and player movement.
LEVEL_MAP = [
'                            ',
'           XXXXXX           ',
'        P                   ',
' XX    XXX            XX    ',
' XX                         ',
' XXXX         XX         XX ',
' XXXX       XX              ',
' XX       XXXX    XX  XX    ',
'       X  XXXX    XX  XXX   ',
'     XXX  XXXXXX  XX  XXXX  ',
'XXXXXXXX  XXXXXX  XX  XXXX  ']

TITLE = "Wizard Of The Valley"

GRAVITY = 0.75
ROWS = 16
COLS = 150
TILE_SIZE = 64
MAX_LEVELS = 3 
level = 1
SCREEN_WIDTH = 1200
BULLET_RATE = 500
SCREEN_HEIGHT = len(LEVEL_MAP) * TILE_SIZE
start_game = False
start_intro = False
FPS = 60

#define colours
BG = (144, 201, 120)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
PINK = (235, 65, 54)
