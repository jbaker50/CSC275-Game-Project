
#im leaving this for u later me, its kinga fucked but whatever. have fun!!

import pygame
import sys
from os import path

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y,):
        super().__init__()
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        self.sprites = []
        self.is_animating = False
        self.idle = True
        self.holding = False
        self.sprites.append(pygame.image.load(path.join(img_folder, 'wizard_00.png')).convert_alpha())
        self.sprites.append(pygame.image.load(path.join(img_folder, 'wizard_01.png')).convert_alpha())
        self.sprites.append(pygame.image.load(path.join(img_folder, 'wizard_02.png')).convert_alpha())
        self.sprites.append(pygame.image.load(path.join(img_folder, 'wizard_03.png')).convert_alpha())
        self.sprites.append(pygame.image.load(path.join(img_folder, 'wizard_04.png')).convert_alpha())
        self.sprites.append(pygame.image.load(path.join(img_folder, 'wizard_05.png')).convert_alpha())
        self.sprites.append(pygame.image.load(path.join(img_folder, 'wizard_06.png')).convert_alpha())
        self.sprites.append(pygame.image.load(path.join(img_folder, 'wizard_07.png')).convert_alpha())
        self.sprites.append(pygame.image.load(path.join(img_folder, 'wizard_08.png')).convert_alpha())
        self.sprites.append(pygame.image.load(path.join(img_folder, 'wizard_09.png')).convert_alpha())
        self.sprites.append(pygame.image.load(path.join(img_folder, 'wizard_10.png')).convert_alpha())
        self.sprites.append(pygame.image.load(path.join(img_folder, 'wizard_11.png')).convert_alpha())
        self.sprites.append(pygame.image.load(path.join(img_folder, 'wizard_12.png')).convert_alpha())
        self.sprites.append(pygame.image.load(path.join(img_folder, 'wizard_13.png')).convert_alpha())
        self.sprites.append(pygame.image.load(path.join(img_folder, 'wizard_14.png')).convert_alpha())
        self.sprites.append(pygame.image.load(path.join(img_folder, 'wizard_15.png')).convert_alpha())
        self.sprites.append(pygame.image.load(path.join(img_folder, 'wizard_16.png')).convert_alpha())
        self.current_sprite = 0
        self.speed = 0.05
        self.length = 2
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        if self.idle == True:
            self.current_sprite = 0
            self.speed = 0.05
            self.length = 2
            self.current_sprite += self.speed
            if self.current_sprite >= self.length:
                self.current_sprite = 0
            self.image = self.sprites[int(self.current_sprite)]

        if self.is_animating == True:
            self.current_sprite += self.speed
            if self.current_sprite >= self.length:
                self.current_sprite = 0
                self.is_animating = False
                self.idle = True
                
            self.image = self.sprites[int(self.current_sprite)]

        

    def animate(self, c, l, s):
        self.current_sprite = c
        self.length = l
        self.speed = s
        self.is_animating = True
        self.idle = False
        

#setup
pygame.init()
clocl = pygame.time.Clock()

#defining game screen
screen_width = 400
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Sprite Animation")

#initializes the objects
player = Player(200, 200)
player_group = pygame.sprite.Group()
player_group.add(player)

#screen event checks
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                c = 8
                l = 11
                s = 0.05
                self.holding = True
                player.animate(c, l, s)
                
            elif event.key == pygame.K_RIGHT:
                print("useless rn :)")
            elif event.key == pygame.K_LEFT:
                print("useless rn :)")
            elif event.key == pygame.K_UP:
                print("useless rn :)")

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                self.holding = False
                print("useless rn :)")
            elif event.key == pygame.K_RIGHT:
                print("useless rn :)")
            elif event.key == pygame.K_LEFT:
                print("useless rn :)")
                
#drawing and initializing
    screen.fill((255, 0, 0))
    player_group.draw(screen)
    player_group.update()
    pygame.display.flip()
    clocl.tick(60)
