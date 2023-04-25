import pygame as pg
import random;
import os
from main import *

class Enemy(pg.sprite.Sprite):
    
    def __init__(self, x, y, scale, speed, mana, slime, newt, frog, reed) -> None:
        '''Put pass in parameters in the construction to inject parameters.
        Ex: location, size, respective map, health, item drops'''
        pg.sprite.Sprite.__init__(self)
        pg.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = speed
        self.scale = scale
        self.mana = mana
        self.slime = slime
        self.newt = newt
        self.frog = frog
        self.reed = reed
        # self.fireballs = fireballs
        self.shoot_cooldown = 0
        self.health = 100
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pg.time.get_ticks()
        #ai specific variables
        self.move_counter = 0
        self.vision = pg.Rect(0, 0, 150, 20)
        self.idling = False
        self.idling_counter = 0
        
        #load all images for the players
        animation_types = ['Idle', 'Run', 'Jump', 'Death']
        for animation in animation_types:
            #reset temporary list of images
            temp_list = []
            #count number of files in the folder
            num_of_frames = len(os.listdir(f'img/enemy/{animation}'))
            for i in range(num_of_frames):
                img = pg.image.load(f'img/enemy/{animation}/{i}.png').convert_alpha()
                img = pg.transform.scale(img, (64,64))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
    
    def ai(self):
        if self.alive :#and player.alive:
            if self.idling == False and random.randint(1, 200) == 1:
                self.update_action(0)#0: idle
                self.idling = True
                self.idling_counter = 50
			#check if the ai in near the player
            # if self.vision.colliderect(player.rect):
            #     #stop running and face the player
            #     self.update_action(0)#0: idle
            #     #shoot
            #     self.shoot()
            else:
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1)#1: run
                    self.move_counter += 1
                    #update ai vision as the enemy moves
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)

                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False

        #scroll
        self.rect.x += screen_scroll
    