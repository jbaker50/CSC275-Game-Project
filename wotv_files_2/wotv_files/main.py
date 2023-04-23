import pygame
from pygame import mixer
from os import path
import random
import sys
#import button
from settings import *
from sprites import *
from tilemap import *
from load import TiledMap
from settings import *
from wotv_files_2.wotv_files.settings import LEVEL_MAP

#setup, initializing variables and screen
#mixer.init()
#pygame.init()
#screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#pygame.display.set_caption(TITLE)
#clock = pygame.time.Clock()
#level = Level(LEVEL_MAP, screen)

class Game:
    def __init__(self):
        mixer.init()
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.start_level = LEVEL_MAP
        self.load_data()
        
    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        map_folder = path.join(game_folder, 'levels')
        self.map = TiledMap(path.join(map_folder, 'swamp_test.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()


    def run(self):
        run = True
        while run:
            self.dt = self.clock.tick(FPS) / 1000.0
            self.events()

            self.screen.fill(RED)
            self.fsfs.run()
            pygame.display.update()

    def events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.exits = pygame.sprite.Group()
        self.fsfs = Level(self.start_level, self.screen)
        # for row, tiles in enumerate(self.map.data):
        #     for col, tile in enumerate(tiles):
        #         if tile == '1':
        #             Wall(self, col, row)
        #         if tile == 'M':
        #             Mob(self, col, row)
        #         if tile == 'P':
        #             self.player = Player(self, col, row)
        #self.camera = Camera(self.map.width, self.map.height)
        #self.draw_debug = False

g = Game()
while True:
    g.new()
    g.run()
    

    #clock.tick(FPS), but this slows down the game running so i dunno

#draw_bg can be added back in, but the background is in the tiled level data atm

#unused atm, here from the og code
def draw_text(text, font, text_col, pos):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_bg():
    pass

def reset_level():
    pass

    
