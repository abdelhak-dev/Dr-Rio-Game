import pygame
from os import path

from pygame.locals import *


pygame.init()
clock = pygame.time.Clock()
fps=60
screen_width = 700
screen_height = 700

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Dangerous Rio Game')

#define game variables
tile_size = 35
game_over = 0
############# """
coin_value = 5
global score
score = 0
font_name = pygame.font.match_font("comicsansms")

#load images

bg_img = pygame.image.load('back.jpg')
win_img = pygame.image.load('you_win.png')
restart_img = pygame.image.load('restart_btn.png')



class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.clicked = False


	def draw(self):
		action = False
		#mouse position
		pos = pygame.mouse.get_pos()

		#chek mousover and clicked condiition
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button
		screen.blit(self.image, self.rect)

		return action






class Player():
	def __init__(self, x, y):
		self.reset(x, y)


	def update(self, game_over):

		dx = 0
		dy = 0
		walk_cooldown = 4
		self.score = 0
		global score


		if game_over == 0 :
			#get keypresses
			key = pygame.key.get_pressed()
			if key[pygame.K_SPACE] and self.jumped ==False and self.in_air == False:
				self.vel_y = -15
				self.jumped = True
			if key[pygame.K_SPACE] == False:
				self.jumped = False
			if key[pygame.K_LEFT]:
				dx -= 5
				self.counter += 1
				self.direction = -1
			if key[pygame.K_RIGHT]:
				dx += 5
				self.counter += 1
				self.direction = 1
			if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
				self.counter = 0
				self.index = 0
				if self.direction == -1:
					self.image = self.images_right[self.index]
				if self.direction == 1:
					self.image = self.images_left[self.index]


			#Animation
			if self.counter > walk_cooldown:
				self.counter = 0
				self.index += 1
				if self.index >= len(self.images_right):
					self.index = 0
				if self.direction == -1:
					self.image = self.images_right[self.index]
				if self.direction == +1:
					self.image = self.images_left[self.index]


			#add gravity
			self.vel_y += 1
			if self.vel_y > 10:
				self.vel_y = 10
			dy += self.vel_y

			#check for collision
			self.in_air = True
			for tile in world.tile_list:
				#check collision x direction:
				if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.hight):
					dx = 0

				#collision dx : #détecter la collusion avant (à l'aide d'un rectangle intérmediere)
				if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.hight):
					#chek collision sur le sol :
					if self.vel_y < 0 :
						dy= tile[1].bottom - self.rect.top
						self.vel_y = 0
					# chek collision sur le sol :
					elif self.vel_y >= 0 :
						dy= tile[1].top - self.rect.bottom
						self.vel_y = 0
						self.in_air = False


			#chek collison with enemy:
			if pygame.sprite.spritecollide(self, blob_group, False):
				game_over = -1

				# chek collison with Lava:
			if pygame.sprite.spritecollide(self, lava_group, False):
				game_over = -1
				print(game_over)

			# chek collison with Coins:
			if pygame.sprite.spritecollide(self, coin_group, True):
				global score
				score += coin_value
				print('score', score)
				#if score == 40:  # game_over == 0 and score == 40 :
					#self.image = self.win_image
					#if self.rect.y > 10:
						#self.rect.y -= 4


			#update player coordinates
			self.rect.x += dx
			self.rect.y += dy
		# Ghost Animation
		elif game_over == -1:
			self.image = self.dead_image
			if self.rect.y > 200:
				self.rect.y -= 5
		"""
		if score == 40 : #game_over == 0 and score == 40 :
			self.image = self.win_image
			if self.rect.y > 10:
				self.rect.y -= 4
		"""
		#draw player onto screen
		screen.blit(self.image, self.rect)
		pygame.draw.rect(screen, (243,249,67), self.rect, 1)
		return game_over


	def reset(self, x, y):
		self.images_right = []
		self.images_left = []
		self.index = 0  # index de comptage
		self.counter = 0
		self.score = 0 #Score

		# Boucle d'animation mouvement droite
		for num in range(1, 10):
			img_right = pygame.image.load(f'img_mod/R{num}.png')
			img_right = pygame.transform.scale(img_right, (30, 55))
			img_left = pygame.transform.flip(img_right, True, False)
			self.images_left.append(img_right)
			self.images_right.append(img_left)
		# Lose_Level image + scale image
		self.dead_image = pygame.image.load('ghost.png')
		self.dead_image = pygame.transform.scale(self.dead_image, (60, 110))

		# Win_Level image + scale image
		self.win_image = pygame.image.load('you_win.png')
		self.win_image = pygame.transform.scale(self.dead_image, (100, 110))

		self.image = self.images_right[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.width = self.image.get_width()
		self.hight = self.image.get_height()
		self.vel_y = 0
		self.jumped = False
		self.direction = 0
		self.in_air = True



def message_to_the_screen(message, color, font_size, x, y):
	#display to the screen
	font = pygame.font.SysFont(font_name, font_size)   #font_name,font size
	text = font.render(message, True, (66,214,145)) #(252,148,50)
	text_rect = text.get_rect()
	text_rect.center = (x, y)
	screen.blit(text, text_rect)




class World():
	def __init__(self, data):
		self.tile_list = []

		#load images
		dirt_img = pygame.image.load('dirt.png')
		grass_img = pygame.image.load('grass.png')

		row_count = 0
		for row in data:
			col_count = 0
			for tile in row:
				if tile == 1:
					img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 2:
					img = pygame.transform.scale(grass_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 3:
					blob = Enemy(col_count * tile_size, row_count * tile_size - 20)
					blob_group.add(blob)
				if tile == 6:
					lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
					lava_group.add(lava)
				if tile ==7:
					coin = Coins(col_count * tile_size, row_count * tile_size + (tile_size // 2))
					coin_group.add(coin)
				col_count += 1
			row_count += 1

	def draw(self):
		for tile in self.tile_list:
			screen.blit(tile[0], tile[1])
			pygame.draw.rect(screen, (255,255,255), tile[1], 2)

class Enemy(pygame.sprite.Sprite):
	def __init__(self, x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('R1E.png')
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.move_direction = 1
		self.move_counter = 0

	def update(self):
		self.rect.x += self.move_direction
		self.move_counter += 1
		if self.move_counter > 20:
			self.move_direction *= -1
			self.move_counter *= -1


		#direction
		self.direction = 0


class Lava(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('Lava_1.png')
		self.image = pygame.transform.scale(img, (tile_size // 2, tile_size * 2))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

class Coins(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('Coins.png')
		self.image = pygame.transform.scale(img, (tile_size, tile_size ))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.score_result  = 0  #self.score = result


world_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1],
[1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 7, 7, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 2, 2, 1],
[1, 0, 0, 0, 0, 0, 3, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1],
[1, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 2, 0, 0, 1],
[1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 2, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 1],
[1, 0, 0, 0, 0, 7, 2, 2, 7, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 1],
[1, 0, 0, 0, 7, 2, 1, 1, 2, 0, 0, 0, 0, 0, 1, 1, 2, 0, 0, 1],
[1, 0, 0, 0, 2, 1, 1, 1, 6, 6, 6, 6, 6, 6, 1, 1, 1, 2, 0, 1],
[1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1]
]



player = Player(100, screen_height - 130)
#Score = Coins (100 ,screen_height -10)
blob_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
world = World(world_data)
#creat button
restart_button = Button(screen_width // 2 - 50, screen_height // 2 + 50, restart_img)

run = True
while run:

	screen.blit(bg_img, (0, 0))
	world.draw()
	#stop enemy while deing
	if game_over == 0:
		blob_group.update()

	#Affichage sur l'écran + score
	blob_group.draw(screen)
	lava_group.draw(screen)
	coin_group.draw(screen)
	message_to_the_screen("Score: " + str(score), screen_width, 30, screen_width /2 ,50)
	game_over = player.update(game_over)
	print(game_over)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

		if score == 40 :
			screen.blit(win_img, (178, 270))


		# if player dead = restart
		if game_over == -1:
			if restart_button.draw():
				player.reset(100, screen_height - 130)
				game_over = 0
				coin_group.update()

	pygame.display.update()
pygame.quit()

clock.tick(fps)