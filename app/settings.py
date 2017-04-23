# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 128, 0)
BLUE = (0, 0, 255)
YELLOW = (160, 160, 0)
GREY = (100, 100, 100)
PURPLE = (128, 0, 128)

COLORKEY = (1, 1, 1)

COLOR_POWER_BAR = (100,50,138)
COLOR_POWER_BAR_EMPTY = (0,0,0,1)

BACKGROUND_COLOR = (255,255,255)

#Main font
FONT_NAME = 'arial'

FPS = 60

#EPSILON
EPS = 0.000001

#DIMENSION
# http://gamedevelopment.tutsplus.com/articles/quick-tip-what-is-the-best-screen-resolution-for-your-game--gamedev-14723
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_WIDTH = 32
TILE_HEIGHT = 32

UPGRADE_SIZE = 96

# Development mode, DEV or OPT
DEV_MODE = 1
OPT_MODE = 0
MODE = DEV_MODE

# To get which mouse button is pressed.
MOUSE_LEFT = 1
MOUSE_RIGHT = 3

#Scenes self.nextScene commands, used to tell SceneHandler what next scene to run after this one ends
TITLE_SCENE = 0
GAME_SCENE = 1
INSTRUCTION_SCENE = 911
CREDIT_SCENE = 777

#Facing Sides
RIGHT = 0
LEFT = 1
UP = 2
DOWN = 3

#LAYERS
COLLISION_LAYER = 0
TERRAIN_LAYER = 2
SPRITE_LAYER = 3
CAMERA_HUD_LAYER = 4

#Collisions
SOLID = 1 #Booléen de GID pour collision
INDESTRUCTIBLE = 2
SPRING = 3
LADDER = 4
SPIKE = 10
NONE = 5 #Pour identifier qu'il n'y a eu aucune collision

#TileTypes
LADDER_TILE = 60

#Tile no
EARTH = 53

OBSTACLE = 100 #This is not a tile

#Player jump states
GROUNDED = 0
JUMP = 1
CLIMBING = 2 #When on a ladder

#Physics
GRAVITY = 1
FRICTION = 1

#Projectiles
GRENADE_SPEEDX = 2
GRENADE_SPEEDY = 2
TARGET_DISTANCE = 30

#PLAYER_STRENGTH
PICKAXE_STRENGTH_LEVEL = (0,1,10,100)
DRILL_STRENGTH_LEVEL = (0,1,10,100)
DYNAMITE_STRENGTH_LEVEL = (0,10,100)

#ENEMY MODE
WALKING = 1
PREPARE_ATTACK = 2
IN_ATTACK = 3

POWER_CAP = 9
RATIO = 5

# Dimension tile base for icon
TILEDIMX = 32
TILEDIMY = 32

# Dimension tile base for enemy
ENEMY_DIMX = 20
ENEMY_DIMY = 20

# Dimension tile base for player
PLAYER_DIMX = 21
PLAYER_DIMY = 21

# End level condition
PLAYER_DEAD = 0
LEVEL_WON = 1
LAST_LEVEL_WON =6

# Mode
PLAYER_DIG_MODE = 0
PLAYER_DRILL_MODE = 1
PLAYER_DYNAMITE_MODE = 1

# Some CD settings
DIG_COOLDOWN = 20
DRILL_COOLDOWN = 10

# Info for gems numbers on terain_set
NB_TSET = 50
ID_GEM = {1: 'GOLD1',
          7: 'GOLD2',
          2: 'PINK1',
          9: 'PINK1',
          8: 'PINK2',
          27: 'PINK2',
          15: 'GREEN1',
          25: 'GREEN1',
          20: 'GREEN2',
          21: 'GREEN2',
          31: 'RED1',
          26: 'RED2'}

# Values of gems
VAL_GOLD1 = 5
VAL_GOLD2 = 10
VAL_PINK1 = 25
VAL_PINK2 = 50
VAL_GREEN1 = 100
VAL_GREEN2 = 200
VAL_RED1 = 1000
VAL_RED2 = 2000

# Music type
MUSIC_OFF = 0
MUSIC_RUN = 1
MUSIC_MUTED = 2
MUSIC_TYPE1 = 1
MUSIC_TYPE2 = 2
MUSIC_HEIGHT_SWITCH = 200

#GUI settings
DIALOG_TEXT_SIZE = 20
INPUT_BOX_FONT = "Arial"
INPUT_BOX_TEXT_SIZE = 20
MENU_FONT = "Arial"

COLOR_MENU_FONTS = WHITE
COLOR_MENU_1 = (50,50,50)
COLOR_MENU_2 = (0,159,0)
COLOR_MENU_SELECT_1 = (255,160,0)
COLOR_MENU_SELECT_2 = BLACK
COLOR_MENU_FONTS_SELECT = BLACK

HUD_FONT_COLOR = COLOR_MENU_FONTS
HUD_FONT_SIZE = 20
HUD_HEIGHT = 40
HUD_COLOR_1 = COLOR_MENU_1
HUD_COLOR_2 = COLOR_MENU_2

FULL_LOAD_COLOR = (0,0,255)
LOADING_COLOR = COLOR_MENU_2

#Buy state
SHOP_AVAILABLE = 0
SHOP_SOLD_OUT = 1
SHOP_REPEATABLE = 2

# If you add a Tag for debugging, you MUST set it here at 0 for everyone
# You can turn your tag on in your own settings_local.py for personal use

TAG_BP = 0
TAG_MARIE = 0
TAG_PHIL = 0
TAP_DIAGNOSE_MAP_TMX = 0

# Load settings_local.py if exist
try:
    from app.settings_local import *
except ImportError:
    pass

# To check the version of some package, one can use
# print(pygame.__version__)
# print(pytmx.__version__)
# print(pyscroll.__version__)
# print(numpy.__version__)
