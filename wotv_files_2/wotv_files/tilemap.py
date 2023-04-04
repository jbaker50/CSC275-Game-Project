import pygame
import pytmx
from sprites import *
from settings import *


class Level:
    def __init__(self, level_data, surface):

        #level setup
        self.display_surface = surface
        self.setup_level(level_data)
        self.shift = 0

    #loads the level data from the settings folder, this could also be used for the tmx if reformatted, and could go in the main file
    def setup_level(self, layout):
        self.floor = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        #self.map = TiledMap(path.join(map_folder, f'level{self.level}.tmx'))
        #self.map_img = self.map.make_map()
        #self.map_rect = self.map_img.get_rect()
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if col == 'X':
                    tile = Tile((x, y), TILE_SIZE)
                    self.floor.add(tile)
                if col == 'P':
                    player_sprite = Player((x, y))
                    self.player.add(player_sprite)

        #for tile_object in self.map.tmxdata.objects:
         #   if tile_object.name == 'player':
         #       player_sprite = Player([tile_object.x, tile_object.y])

    #handeles the screen scroll. There isn't any screen scrolling for the y atm, but that would be easy
    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < SCREEN_WIDTH/4 and direction_x < 0:
            self.shift = 8
            player.speed = 0
        elif player_x > SCREEN_WIDTH - (SCREEN_WIDTH/4) and direction_x > 0:
            self.shift = -8
            player.speed = 0
        else:
            self.shift = 0
            player.speed = 8

    #collisions could also be moved to the main file if needed
    def horizontal_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.floor.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left

    def vertical_collision(self):
        player = self.player.sprite
        player.move()

        for sprite in self.floor.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.isJumping = False
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0

    #this can also be moved back to the main to go in a Game class if needed, this is basically where the game runs at          
    def run(self):
        self.floor.update(self.shift)
        self.floor.draw(self.display_surface)
        self.scroll_x()
        
        self.player.update()
        self.horizontal_collision()
        self.vertical_collision()
        self.player.draw(self.display_surface)
        

