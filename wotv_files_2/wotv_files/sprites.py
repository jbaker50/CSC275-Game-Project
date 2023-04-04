import pygame
import os
from settings import *
from load import import_folder

#creates the player class. pos includes both x and y coordinates.
class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.01
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(center = pos)

        #player movement settings
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.jump_height = -20

        #player status settings
        self.status = 'idle'
        self.anim_hold = False
        self.isJumping = False
        self.isCharging = False
        self.firing = False
        self.facingRight = True
        self.hurt = False
        self.health = 6
        self.max_health = self.health

    #calls from load to create all of the animation lists. Same logic could be used for enemies.
    def import_character_assets(self):
        character_path = './img/player/'
        self.animations = {'idle':[], 'walk':[], 'jump':[], 'charge':[], 'shoot':[], 'hurt':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    #runs the animation logic. anim_hold is for animations that need to pause on the last frame, such as charge and jump
    def animate(self):
        animation = self.animations[self.status]
        
        if self.anim_hold:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(animation):
                self.frame_index = len(animation) - 1
        else:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(animation):
                self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.facingRight:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image

    #runs the movement for the player. could be moved back to main folder with the while section if needed.
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facingRight = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facingRight = False
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and not self.isJumping:
            self.direction.y = self.jump_height
            self.isJumping = True

        if keys[pygame.K_LSHIFT] and not self.isJumping:
            self.isCharging = True
        else:
            self.isCharging = False

        if keys[pygame.K_h]:
            self.firing = True
        else:
            self.firing = False

        if keys[pygame.K_d]:
            self.hurt = True
        else:
            self.hurt = False

        

        self.direction.y += GRAVITY
        self.rect.y += self.direction.y

    #changes the state of the animation and its settings
    def get_status(self):
        if self.hurt:
            self.status = 'hurt'
            self.animation_speed = 0.2
            self.anim_hold = False
        else:
            if self.isJumping:
                self.status = 'jump'
                self.animation_speed = 0.5
                self.anim_hold = True
            else:
                if self.isCharging:
                    self.status = 'charge'
                    self.animation_speed = 0.04
                    self.anim_hold = True
                else:
                    if self.firing:
                        self.status = 'shoot'
                        self.animation_speed = 0.2
                        self.animation_hold = False
                    else:
                        if self.direction.x != 0:
                            self.status = 'walk'
                            self.animation_speed = 0.1
                            self.anim_hold = False
                        else:
                            self.status = 'idle'
                            self.animation_speed = 0.01
                            self.anim_hold = False

    #updates the player sprite
    def update(self):
        self.get_status()
        self.animate()

    #for the tiles in the map, may be moved for the tmx data if needed
class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(topleft = pos)

    def update(self, x_shift):
        self.rect.x += x_shift

