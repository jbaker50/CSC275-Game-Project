import pygame as pg
import random
from settings import *
from sprites import *
from os import path

FLOOR = (0, HEIGHT - 40, WIDTH, 40)

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)

    def new(self):
        # start a new game
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        # check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0

        # if player reaches left 1/4 of screen
        if self.player.rect.left <= WIDTH / 4:
            self.player.pos.x += abs(self.player.vel.x)
            for plat in self.platforms:
                plat.rect.x += abs(self.player.vel.x)
                #if plat.rect.top >= HEIGHT:
                 #   plat.kill() 
                 #   self.score += 10
                 
        if self.player.rect.right >= 3*(WIDTH / 4):
            self.player.pos.x -= abs(self.player.vel.x)
            for plat in self.platforms:
                plat.rect.x -= abs(self.player.vel.x)
                #if plat.rect.top >= HEIGHT:
                 #   plat.kill() 
                 #   self.score += 10
        
        
        
                 
        # if player reaches right 1/4 of screen

        # Die!
        # rework this later to work with getting hit by enemy
        #if self.player.rect.bottom > HEIGHT:
           # for sprite in self.all_sprites:
                #sprite.rect.y -= max(self.player.vel.y, 10)
                #if sprite.rect.bottom < 0:
                   # sprite.kill()
        #if len(self.platforms) == 0:
            #self.playing = False

        # spawn new platforms to keep same average number
        #while len(self.platforms) < 6:
            #width = random.randrange(50, 700)
            #p = plat
        #                 random.randrange(-75, -30),
        #                 width, 20)
        #    self.platforms.add(p)
        #    self.all_sprites.add(p)

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
                    
            if event.type == CHANGE_PLATFORMS:
                    plats = [FLOOR]
                    #self.new(plats=plats)

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        #self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
       # self.draw_text("Click to start level", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        # game over/continue
        if not self.running:
            return
        self.screen.fill(BGCOLOR)
        
        #self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        #self.draw_text("Click to retry level", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        #pg.display.flip()
        #self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
