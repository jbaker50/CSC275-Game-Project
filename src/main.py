from turtle import _Screen
from matplotlib.font_manager import get_font
import pygame
from pygame import mixer
import os
import random
import csv
import button
from settings import *
vec = pygame.math.Vector2

# Sound effect come from:
# https://mixkit.co/free-sound-effects/game/

LEVEL = 1

mixer.init()
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)

#set framerate
clock = pygame.time.Clock()
FPS = 60

#define player action variables
moving_left = False
moving_right = False
shoot = False

#load music and sounds
pygame.mixer.music.load('audio/background_music.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1, 0.0, 5000)
jump_fx = pygame.mixer.Sound('audio/jump.wav')
jump_fx.set_volume(0.05)
shot_fx = pygame.mixer.Sound('audio/shoot.wav')
shot_fx.set_volume(0.05)

health_and_mana_fx = pygame.mixer.Sound('audio/health_and_mana.wav')
health_and_mana_fx.set_volume(0.2)
pickup_items_fx = pygame.mixer.Sound('audio/pickup_items.wav')
pickup_items_fx.set_volume(0.3)
enemy_death_fx = pygame.mixer.Sound('audio/enemy_death.wav')
enemy_death_fx.set_volume(0.3)
character_death_fx = pygame.mixer.Sound('audio/character_death.wav')
character_death_fx.set_volume(0.8)

#load images
#button images
start_img = pygame.image.load('img/start_btn.png').convert_alpha()
exit_img = pygame.image.load('img/exit_btn.png').convert_alpha()
restart_img = pygame.image.load('img/restart_btn.png').convert_alpha()

#background
layer0 = pygame.image.load('levels/swamp_resources/2 Background/Layers/0.png').convert_alpha()
layer1 = pygame.image.load('levels/swamp_resources/2 Background/Layers/1.png').convert_alpha()
layer2 = pygame.image.load('levels/swamp_resources/2 Background/Layers/2.png').convert_alpha()
layer3 = pygame.image.load('levels/swamp_resources/2 Background/Layers/3.png').convert_alpha()
layer4 = pygame.image.load('levels/swamp_resources/2 Background/Layers/4.png').convert_alpha()
#store tiles in a list
img_list = []
for x in range(TILE_TYPES):
	img = pygame.image.load(f'img/tile/{x}.png')
	img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
	img_list.append(img)
#bullet
bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()
#pick up boxes

health_box_img = pygame.image.load('img/tile/19.png').convert_alpha()
mana_box_img = pygame.image.load('img/tile/17.png').convert_alpha()
slime_drop_img = pygame.image.load('img/tile/26.png').convert_alpha()
ghost_drop_img = pygame.image.load('img/tile/26.png').convert_alpha()
bat_drop_img = pygame.image.load('img/tile/26.png').convert_alpha()
newt_img = pygame.image.load('img/tile/21.png').convert_alpha()
frog_img = pygame.image.load('img/tile/22.png').convert_alpha()
reed_img = pygame.image.load('img/tile/23.png').convert_alpha()


item_boxes = {
	'Health'	: health_box_img,
	'Mana'		: mana_box_img,
	'Slime'		: slime_drop_img,
	'Newt'		: newt_img,
	'Frog'		: frog_img,
	'Reed'		: reed_img,
	'Ectoplasm' : ghost_drop_img,
	'Bat Wing'	: bat_drop_img
}

power_ups = {
	'High Jump'	: health_box_img,
	'Fast Run'	: health_box_img,
	'Slow Fall'	: health_box_img
}

#define font
font = pygame.font.SysFont('Futura', 30)

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))


def draw_bg():
	screen.fill(BG)
	width = layer0.get_width()
	for x in range(5):
		screen.blit(layer0, ((x * width) - bg_scroll, 0))
		screen.blit(layer1, ((x * width) - bg_scroll, 0))
		screen.blit(layer2, ((x * width) - bg_scroll, 0))
		screen.blit(layer4, ((x * width) - bg_scroll, 0))
 

#function to reset level
def reset_level():
	enemy_group.empty()
	bullet_group.empty()
	item_box_group.empty()
	decoration_group.empty()
	water_group.empty()
	exit_group.empty()
	
	#create empty tile list
	data = []
	for row in range(ROWS):
		r = [-1] * COLS
		data.append(r)

	return data

class Wizard(pygame.sprite.Sprite):
	def __init__(self, char_type, x, y, scale, speed, mana, slime, newt, frog, reed, ectoplasm, bat_wing, dropped):
		pygame.sprite.Sprite.__init__(self)
		self.currentLevel = 1
		self.alive = True
		self.char_type = char_type
		self.speed = speed
		self.scale = scale
		self.mana = mana
		self.slime = slime
		self.newt = newt
		self.frog = frog
		self.reed = reed
		self.ectoplasm = ectoplasm
		self.bat_wing = bat_wing
		self.shoot_cooldown = 0
		self.health = 100
		self.max_health = self.health
		self.direction = 1
		self.vel_y = 0
		self.jump = False
		self.in_air = True
		self.flip = False
		self.dropped = False
		self.animation_list = []
		self.frame_index = 0
		self.action = 0
		self.update_time = pygame.time.get_ticks()
		#ai specific variables
		self.move_counter = 0
		self.vision = pygame.Rect(0, 0, 150, 20)
		self.idling = False
		self.idling_counter = 0
		self.damageCooldown = 0
		self.timeSinceLastHit = 0
		self.itemsGotten = 0
		self.jumpPowerUp = False
		self.speedPowerUp = False
		self.fallPowerUp = False
		self.slimesKilled = 0
		self.batsKilled = 0
		self.ghostsKilled = 0
  
		if self.char_type == 'Slime':
			self.health = 100
		if self.char_type == 'Ghost':
			self.health = 150
		if self.char_type == 'Bat':
			self.health = 200
			self.speed = 5
		
		#load all images for the players
		animation_types = ['Idle', 'Run', 'Jump', 'Death']
		for animation in animation_types:
			#reset temporary list of images
			temp_list = []
			#count number of files in the folder
			num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
			for i in range(num_of_frames):
				img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()
				img = pygame.transform.scale(img, (64,64))
				temp_list.append(img)
			self.animation_list.append(temp_list)

		self.image = self.animation_list[self.action][self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.width = self.image.get_width()
		self.height = self.image.get_height()


	def update(self):
		self.update_animation()
		self.check_alive()
		if self.slimesKilled >= 5:
			self.jumpPowerUp = True
   
		if self.ghostsKilled >= 3:
			self.fallPowerUp = True
   
		if self.batsKilled >= 2:
			self.speedPowerUp = True
		#update cooldown
		if self.shoot_cooldown > 0:
			self.shoot_cooldown -= 1

	def disableAllPowerups(self) -> None:
		self.fallPowerUp = self.jumpPowerUp = self.speedPowerUp = False

	def move(self, moving_left, moving_right):
		#reset movement variables
		screen_scroll = 0
		dx = 0
		dy = 0

		#assign movement variables if moving left or right
		if moving_left:
			dx = (-self.speed - 5) if self.speedPowerUp else -self.speed
			self.flip = True
			self.direction = -1
		if moving_right:
			dx = self.speed + 5 if self.speedPowerUp else self.speed
			self.flip = False
			self.direction = 1

		#jump
		if self.jump == True and self.in_air == False:
			self.vel_y = -11 if (not self.jumpPowerUp) and not self.fallPowerUp else -22
			self.jump = False
			self.in_air = True

		#apply gravity
		self.vel_y = self.vel_y + GRAVITY
		if self.vel_y > 10:
			self.vel_y
   
		dy += self.vel_y // 3 if self.fallPowerUp else self.vel_y

		#check for collision
		for tile in world.obstacle_list:
			#check collision in the x direction
			if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
				dx = 0
				#if the ai has hit a wall then make it turn around
				if self.char_type == 'Slime' or self.char_type == 'Ghost' or self.char_type == 'Bat':
					self.direction *= -1
					self.move_counter = 0
			#check for collision in the y direction
			if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
				#check if below the ground, i.e. jumping
				if self.vel_y < 0:
					self.vel_y = 0
					dy = tile[1].bottom - self.rect.top
				#check if above the ground, i.e. falling
				elif self.vel_y >= 0:
					self.vel_y = 0
					self.in_air = False
					dy = tile[1].top - self.rect.bottom


		#check for collision with water
		if pygame.sprite.spritecollide(self, water_group, False):
			self.health = 0

		#check for collision with exit
		level_complete = False

		if pygame.sprite.spritecollide(self, exit_group, False) and player.itemsGotten >= 3:
			player.disableAllPowerups()
			level_complete = True
   

		#check if fallen off the map
		if self.rect.bottom > SCREEN_HEIGHT:
			self.health = 0

		#check if going off the edges of the screen
		if self.char_type == 'player':
			if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
				dx = 0

		#update rectangle position
		self.rect.x += dx
		self.rect.y += dy

		#update scroll based on player position
		if self.char_type == 'player':
			if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE) - SCREEN_WIDTH)\
				or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
				self.rect.x -= dx
				screen_scroll = -dx

		return screen_scroll, level_complete

	def shoot(self):
		if self.shoot_cooldown == 0 and self.mana > 0:
			self.shoot_cooldown = 20
			bullet = Bullet(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
			bullet_group.add(bullet)
			#reduce mana
			self.mana -= 1
			shot_fx.play()

	def ai(self):
		if self.alive and player.alive:
			if self.rect.colliderect(player.rect) and self.damageCooldown == 0:
				if self.char_type == 'Slime':
					player.health -= 10
				if self.char_type == 'Ghost':
					player.health -= 20
				if self.char_type == 'Bat':
					player.health -= 30
				self.timeSinceLastHit = 0
	
			self.damageCooldown = ((self.damageCooldown + 1) % 100)
			self.timeSinceLastHit += 1
   
			if self.timeSinceLastHit > 100:
				self.damageCooldown = 0
    
			if self.idling == False and random.randint(1, 200) == 1:
				self.update_action(0)#0: idle
				self.idling = True
				self.idling_counter = 50
			#check if the ai in near the player
			#if self.vision.colliderect(player.rect):
				#stop running and face the player
				#self.update_action(1)#0: idle
				#self.speed(50)
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

	def update_animation(self):
		#update animation
		ANIMATION_COOLDOWN = 100
		#update image depending on current frame
		self.image = self.animation_list[self.action][self.frame_index]
		#check if enough time has passed since the last update
		if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
			self.update_time = pygame.time.get_ticks()
			self.frame_index += 1
		#if the animation has run out the reset back to the start
		if self.frame_index >= len(self.animation_list[self.action]):
			if self.action == 3:
				self.frame_index = len(self.animation_list[self.action]) - 1
			else:
				self.frame_index = 0

	def update_action(self, new_action):
		#check if the new action is different to the previous one
		if new_action != self.action:
			self.action = new_action
			#update the animation settings
			self.frame_index = 0
			self.update_time = pygame.time.get_ticks()

	def check_alive(self):
		if self.health <= 0:
			self.health = 0
			self.speed = 0
			self.alive = False
			self.update_action(3)
   
   
	def kill(self) -> None:
		if self.char_type != 'slime':
			return 

		rng = random.random()
		if rng >= .5 and player.slime == 0:
			player.slime += 1
			player.itemsGotten += 1
			player.update()
   
		rng = random.random()
		if rng >= .5 and player.ectoplasm == 0:
			player.ghostsKilled += 1
			player.itemsGotten += 1
			player.update()
	
		rng = random.random()
		if rng >= .5 and player.bat_wing == 0:
			player.batsKilled += 1
			player.itemsGotten += 1
			player.update()
   
		#print(f'RNG Seed: {rng}')
		#print(f'Player item count: {player.itemsGotten}')

	def draw(self):
		screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

class World():
	def __init__(self):
		self.obstacle_list = []

	def process_data(self, data):
		self.level_length = len(data[0])
		#iterate through each value in level data file
		for y, row in enumerate(data):
			for x, tile in enumerate(row):
				if tile >= 0:
					img = img_list[tile]
					img_rect = img.get_rect()
					img_rect.x = x * TILE_SIZE
					img_rect.y = y * TILE_SIZE
					tile_data = (img, img_rect)
					if tile >= 0 and tile <= 8:
						self.obstacle_list.append(tile_data)
					elif tile >= 9 and tile <= 10:
						water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
						water_group.add(water)
					elif tile >= 11 and tile <= 14:
						decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
						decoration_group.add(decoration)
					elif tile == 15:#create player
						player = Wizard('player', x * TILE_SIZE, y * TILE_SIZE, 1.65, 5, 20, 0, 0, 0, 0, 0, 0, False)
						health_bar = HealthBar(10, 10, player.health, player.health)
					elif tile == 16:#create enemies
						enemy = Wizard('Slime', x * TILE_SIZE, y * TILE_SIZE, 1.65, 2, 20, 0, 0, 0, 0, 0, 0, False)
						enemy_group.add(enemy)
					elif tile == 17:#create mana box
						item_box = ItemBox('Mana', x * TILE_SIZE, y * TILE_SIZE)
						item_box_group.add(item_box)
					elif tile == 18:#create slime box
						item_box = ItemBox('Slime', x * TILE_SIZE, y * TILE_SIZE)
						item_box_group.add(item_box)
					elif tile == 19:#create health box
						item_box = ItemBox('Health', x * TILE_SIZE, y * TILE_SIZE)
						item_box_group.add(item_box)
					elif tile == 20:#create exit
						exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
						exit_group.add(exit)
					elif tile == 21:#create newt
						item_box = ItemBox('Newt', x * TILE_SIZE, y * TILE_SIZE)
						item_box_group.add(item_box)
					elif tile == 22:#create frogS
						item_box = ItemBox('Frog', x * TILE_SIZE, y * TILE_SIZE)
						item_box_group.add(item_box)
					elif tile == 23:#create reed
						item_box = ItemBox('Reed', x * TILE_SIZE, y * TILE_SIZE)
						item_box_group.add(item_box)
					elif tile == 24:#create ectoplasm
						item_box = ItemBox('Ectoplasm', x * TILE_SIZE, y * TILE_SIZE)
						item_box_group.add(item_box)
					elif tile == 25:#create bat wing
						item_box = ItemBox('Bat Wing', x * TILE_SIZE, y * TILE_SIZE)
						item_box_group.add(item_box)
					elif tile == 26:#create ghost enemy
						enemy = Wizard('Ghost', x * TILE_SIZE, y * TILE_SIZE, 1.65, 2, 20, 0, 0, 0, 0, 0, 0, False)
						enemy_group.add(enemy)
					elif tile == 27:#create bat enemy
						enemy = Wizard('Bat', x * TILE_SIZE, y * TILE_SIZE, 1.65, 2, 100, 0, 0, 0, 0, 0, 0, False)
						enemy_group.add(enemy)

		return player, health_bar


	def draw(self):
		for tile in self.obstacle_list:
			tile[1][0] += screen_scroll
			screen.blit(tile[0], tile[1])
   
class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y, direction):
		pygame.sprite.Sprite.__init__(self)
		self.speed = 10
		self.image = bullet_img
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.direction = direction

	def update(self):
		#move bullet
		self.rect.x += (self.direction * self.speed) + screen_scroll
		#check if bullet has gone off screen
		if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
			self.kill()
		#check for collision with level
		for tile in world.obstacle_list:
			if tile[1].colliderect(self.rect):
				self.kill()

		#check collision with characters
		if pygame.sprite.spritecollide(player, bullet_group, False):
			if player.alive:
				player.health -= 5

				if player.health <= 0:
					player.kill()
					character_death_fx.play()
 
				self.kill()
    
		for enemy in enemy_group:
			if pygame.sprite.spritecollide(enemy, bullet_group, False):
				if enemy.alive:
					enemy.health -= 25
	
					if enemy.health <= 0:
						enemy.kill()
						enemy_death_fx.play()

						if enemy.char_type == 'Slime': 
							player.slimesKilled += 1
       
						elif enemy.char_type == 'Ghost':
							player.ghostsKilled += 1
       
						elif enemy.char_type == 'Bat':
							player.batsKilled += 1
       
					self.kill()

class Decoration(pygame.sprite.Sprite):
	def __init__(self, img, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = img
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

	def update(self):
		self.rect.x += screen_scroll

class Water(pygame.sprite.Sprite):
	def __init__(self, img, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = img
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

	def update(self):
		self.rect.x += screen_scroll

class Exit(pygame.sprite.Sprite):
	def __init__(self, img, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = img
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

	def update(self):
		self.rect.x += screen_scroll

class ItemBox(pygame.sprite.Sprite):
	def __init__(self, item_type, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.item_type = item_type
		self.image = item_boxes[self.item_type]
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))


	def update(self):
		#scroll
		self.rect.x += screen_scroll
		#check if the player has picked up the box
		if pygame.sprite.collide_rect(self, player):
			#check what kind of box it was
			if self.item_type == 'Health':
				player.health += 25
				if player.health > player.max_health:
					player.health = player.max_health
				health_and_mana_fx.play()
			elif self.item_type == 'Mana':
				player.mana += 15
				health_and_mana_fx.play()
			#elif self.item_type == 'Slime':
			#	self.dropped = False
			#	player.itemsGotten += 1
			elif self.item_type == 'Newt':
				player.newt += 1
				player.itemsGotten += 1
				pickup_items_fx.play()
			elif self.item_type == 'Frog':
				player.frog += 1
				player.itemsGotten += 1
				pickup_items_fx.play()
			elif self.item_type == 'Reed':
				player.reed += 1
				player.itemsGotten += 1
				pickup_items_fx.play()
			# in the second level
			#elif self.item_type == 'Ectoplasm':
			#	player.ectoplasm += 1
			#	player.itemsGotten += 1
			# in the third level
			#elif self.item_type == 'Bat Wing':
			#	player.ectoplasm += 1
			#	player.itemsGotten += 1

			#delete the item box
			#print(f'Items gotten: {player.itemsGotten}')
			self.kill()

class HealthBar():
	def __init__(self, x, y, health, max_health):
		self.x = x
		self.y = y
		self.health = health
		self.max_health = max_health

	def draw(self, health):
		#update with new health
		self.health = health
		#calculate health ratio
		ratio = self.health / self.max_health
		pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 154, 24))
		pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
		pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))

class ScreenFade():
	def __init__(self, direction, colour, speed):
		self.direction = direction
		self.colour = colour
		self.speed = speed
		self.fade_counter = 0


	def fade(self):
		fade_complete = False
		self.fade_counter += self.speed
		if self.direction == 1:#whole screen fade
			pygame.draw.rect(screen, self.colour, (0 - self.fade_counter, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))
			pygame.draw.rect(screen, self.colour, (SCREEN_WIDTH // 2 + self.fade_counter, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
			pygame.draw.rect(screen, self.colour, (0, 0 - self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
			pygame.draw.rect(screen, self.colour, (0, SCREEN_HEIGHT // 2 +self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT))
		if self.direction == 2:#vertical screen fade down
			pygame.draw.rect(screen, self.colour, (0, 0, SCREEN_WIDTH, 0 + self.fade_counter))
		if self.fade_counter >= SCREEN_WIDTH:
			fade_complete = True

		return fade_complete

#create screen fades
intro_fade = ScreenFade(1, BLACK, 4)
death_fade = ScreenFade(2, PINK, 4)

#create buttons
start_button = button.Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 150, start_img, 1)
exit_button = button.Button(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 100, exit_img, 1)
restart_button = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, restart_img, 2)

#create sprite groups
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

#create empty tile list
world_data = []
for row in range(ROWS):
	r = [-1] * COLS
	world_data.append(r)
#load in level data and create world
with open(f'level{level}_data.csv', newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	for x, row in enumerate(reader):
		for y, tile in enumerate(row):
			world_data[x][y] = int(tile)
world = World()
player, health_bar = world.process_data(world_data)

run = True
while run:

	clock.tick(FPS)

	if start_game == False:
		#draw menu
		screen.fill(BG)
		#add buttons
		if start_button.draw(screen):
			start_game = True
			start_intro = True
		if exit_button.draw(screen):
			run = False
	else:
		#update background
		draw_bg()
		#draw world map
		world.draw()
		#show player health
		health_bar.draw(player.health)
		#show mana
		draw_text('MANA: ', font, WHITE, 10, 35)
		for x in range(player.mana):
			screen.blit(bullet_img, (90 + (x * 10), 40))
		draw_text('NEWT: ', font, WHITE, 10, 60)
		for x in range(player.newt):
			screen.blit(newt_img, (70 + (x * 15), 55))
		# show frog pickup
		draw_text('FROG: ', font, WHITE, 10, 95)
		for x in range(player.frog):
			screen.blit(frog_img, (70 + (x * 15), 90))
		# show reed pickup
		draw_text('REED: ', font, WHITE, 10, 125)
		for x in range(player.reed):
			screen.blit(reed_img, (70 + (x * 15), 120))


		player.update()
		player.draw()

		for slime in enemy_group:
			slime.ai()
			slime.update()
			slime.draw()

		#update and draw groups
		bullet_group.update()
		item_box_group.update()
		decoration_group.update()
		water_group.update()
		exit_group.update()
		bullet_group.draw(screen)
		item_box_group.draw(screen)
		decoration_group.draw(screen)
		water_group.draw(screen)
		exit_group.draw(screen)

		#show intro
		if start_intro == True:
			if intro_fade.fade():
				start_intro = False
				intro_fade.fade_counter = 0

		#update player actions
		if player.alive:
			#shoot bullets
			if shoot:
				player.shoot()
			if player.in_air:
				player.update_action(2)#2: jump
			elif moving_left or moving_right:
				player.update_action(1)#1: run
			else:
				player.update_action(0)#0: idle
			screen_scroll, level_complete = player.move(moving_left, moving_right)
			bg_scroll -= screen_scroll
			#check if player has completed the level
			if level_complete:
				start_intro = True
				level += 1
				bg_scroll = 0
				world_data = reset_level()
				if level <= MAX_LEVELS:
					#load in level data and create world
					with open(f'level{level}_data.csv', newline='') as csvfile:
						reader = csv.reader(csvfile, delimiter=',')
						for x, row in enumerate(reader):
							for y, tile in enumerate(row):
								world_data[x][y] = int(tile)
					world = World()
					player, health_bar = world.process_data(world_data)	
		else:
			screen_scroll = 0
			if death_fade.fade():
				if restart_button.draw(screen):
					death_fade.fade_counter = 0
					start_intro = True
					bg_scroll = 0
					world_data = reset_level()
					#load in level data and create world
					with open(f'level{level}_data.csv', newline='') as csvfile:
						reader = csv.reader(csvfile, delimiter=',')
						for x, row in enumerate(reader):
							for y, tile in enumerate(row):
								world_data[x][y] = int(tile)
					world = World()
					player, health_bar = world.process_data(world_data)

	for event in pygame.event.get():
		#quit game
		if event.type == pygame.QUIT:
			run = False
		#keyboard presses
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_0:
				player.fallPowerUp = not player.fallPowerUp
    
			if event.key == pygame.K_a:
				moving_left = True
			if event.key == pygame.K_d:
				moving_right = True
			if event.key == pygame.K_SPACE:
				shoot = True
			if event.key == pygame.K_w and player.alive:
				player.jump = True
				jump_fx.play()
			if event.key == pygame.K_ESCAPE:
				run = False

		#keyboard button released
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_a:
				moving_left = False
			if event.key == pygame.K_d:
				moving_right = False
			if event.key == pygame.K_SPACE:
				shoot = False

	pygame.display.update()

pygame.quit()