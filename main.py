import pygame
from pygame.locals import *
import pickle
from os import path

"""
Le jeux Dr Rio est un jeux inspiré du jeux clasique Super Mario. Le docteur Rio est un scientifique qui mène 
des experiences de modification du code génetique. Un jour il a créer par hasard des monstres totalement incontrolables..
il a décider de les viccre lui meme et proccurer à lui le devis le plus chère , c'est les pièces d'ors "Rio" .

Le programme main contient 3 classes principal : 
1) Class Player
	Cette classe contient les mouvements de controles pour le joueur via la fonction update(),ainsi que son animation.
	La fonction reset permet d'actualiser le niveau si le joueur meur.
	game_over c'est une varible d'execution du jeux :
	 si game_over = 0 (mode jeux)
	 	game_over = -1 (joueur mort ,donc le jeux redemare si l'utilisateur le souhaite bien sur)
		game_over = 1 le jeux s'execute 
		
	La fonction score_tag et level_tag s'occupe de la partie affichage de niveau et du score
		
2) Class World
	Cette classe contient la partie gestion de collision avec la map (monstres,lava ,Sortie).
	L'importation de la map se fait en appelant à la library Pickel àfin de sauvgarder la map (level1 & level2) sur le disque dur,
	La partie import est export (manuel) est dans le fichier "to_pickel.py"
	
	
3) Class Enemy 
	les monstres avec leurs mouvement 
+
4) Class Lava 
5) Class Exit
6) la class Button c'est pour la création des boutons "Restat" , "Start" , "Exit"
7) Classe Coins pour la création des pièces d'or

"""

pygame.init()
clock = pygame.time.Clock()
fps=60
#Réglage de l'écran :
screen_width = 700
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Dr Rio Game')

#define game variables
tile_size = 35
game_over = 0
main_menue = True
level = 1
max_levels = 2
############# """
coin_value = 5
global score
score = 0
max_levels = 2
font_name = pygame.font.match_font("comicsansms")

#load images
bg_img = pygame.image.load('./img/back.jpg')
win_img = pygame.image.load('./img/you_win.png')
restart_img = pygame.image.load('./img/restart_btn.png')
start_img = pygame.image.load('./img/start_btn.png')
pause_img = pygame.image.load('./img/pause_btn.png')
#logo_standing = pygame.image.load('standing.png')
exit_img = pygame.image.load('./img/exit_btn.png')



#function to reset

def reset_level(level):
	player.reset(100, screen_height - 130)
	blob_group.empty()
	lava_group.empty()
	exit_group.empty()

	#load in leevl data and create wold
	if path.exists(f'level{level}_data'):
		pickle_in = open(f'level{level}_data', 'rb')
		world_data = pickle.load(pickle_in)
	world = World(world_data)
	return world



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

			if pygame.sprite.spritecollide(self,exit_group, False):
				if level == 1 :
					if score >= 45 :
						game_over = 1
				elif level == 2 :
						if score >= 90 :
							game_over = 1


			#update player coordinates
			self.rect.x += dx
			self.rect.y += dy
		# Ghost Animation
		elif game_over == -1:
			self.image = self.dead_image
			if self.rect.y > 200:
				self.rect.y -= 5

		#draw player onto screen
		screen.blit(self.image, self.rect)
		#pygame.draw.rect(screen, (243,249,67), self.rect, 1) == cadrrage du joueur
		return game_over


	def reset(self, x, y):
		self.images_right = []
		self.images_left = []
		self.index = 0  # index de comptage
		self.counter = 0
		self.score = 0 #Score
		self.level = level

		# Boucle d'animation mouvement droite
		for num in range(1, 10):
			img_right = pygame.image.load(f'img_mod/R{num}.png')
			img_right = pygame.transform.scale(img_right, (30, 55))
			img_left = pygame.transform.flip(img_right, True, False)
			self.images_left.append(img_right)
			self.images_right.append(img_left)
		# Lose_Level image + scale image
		self.dead_image = pygame.image.load('./img/ghost.png')
		self.dead_image = pygame.transform.scale(self.dead_image, (60, 110))

		# Win_Level image + scale image
		self.win_image = pygame.image.load('./img/you_win.png')
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



def score_tag(message, color, font_size, x, y):
	#display to the screen
	font = pygame.font.SysFont(font_name, font_size)   #font_name,font size
	text = font.render(message, True, (66,214,145)) #(252,148,50)
	text_rect = text.get_rect()
	text_rect.center = (x, y)
	screen.blit(text, text_rect)

def level_tag(message, color, font_size, x, y):
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
		dirt_img = pygame.image.load('./img/dirt.png')
		grass_img = pygame.image.load('./img/grass.png')

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
				if tile == 8:
					exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 3))
					exit_group.add(exit)
				col_count += 1
			row_count += 1

	def draw(self):
		for tile in self.tile_list:
			screen.blit(tile[0], tile[1])
			pygame.draw.rect(screen, (255,255,255), tile[1], 2)

class Enemy(pygame.sprite.Sprite):
	def __init__(self, x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('./img/R1E.png')
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
		img = pygame.image.load('./img/Lava_1.png')
		self.image = pygame.transform.scale(img, (tile_size, tile_size // 1))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

class Coins(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('./img/Coins.png')
		self.image = pygame.transform.scale(img, (tile_size, tile_size ))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.score_result  = 0  #self.score = result

class Exit(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('./img/exit.png')
		self.image = pygame.transform.scale(img, (tile_size , int(tile_size + 12)))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y


player = Player(100, screen_height - 130)
blob_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
#load path
if path.exists(f'level{level}_data'):
	pickle_in = open(f'level{level}_data', 'rb')
	world_data = pickle.load(pickle_in)
world = World(world_data)


#creat button
restart_button = Button(screen_width // 2 - 50, screen_height // 2 + 50, restart_img)
start_button = Button(screen_width // 4 - 100, screen_height // 2, start_img)
pause_button = Button(screen_width // 2 - 30, screen_height // 2 + 60, restart_img)
exit_button = Button(screen_width // 2 + 100, screen_height // 2, exit_img)
#logo_standing = Button(screen_width //1 +40, screen_height // 3, logo_standing)

run = True
while run:

	clock.tick(fps)
	screen.blit(bg_img, (0, 0))
	#buttons
	if main_menue == True:
		#logo_standing.draw()  # draw logo
		if exit_button.draw() == True:
			run = False
		if start_button.draw():
			main_menue = False
	else:

		world.draw()
		# screen.blit(pause_img, (550, 36)) # Il manque la fonctionalité Pause pour ce bouton

		#stop enemy while deing
		if game_over == 0:
			level = level
			blob_group.update()
		#Affichage sur l'écran + score
		blob_group.draw(screen)
		lava_group.draw(screen)
		coin_group.draw(screen)
		exit_group.draw(screen)
		score_tag("Score: " + str(score), screen_width, 30, screen_width /2 ,50)
		level_tag("Level: " + str(level), screen_width, 30, screen_width //5.5 ,50)

		game_over = player.update(game_over)
		print(game_over)
		# if player dead = restart
		if game_over == -1:
			if restart_button.draw():
				world_data = []
				world = reset_level(level)
				game_over = 0
				score = 0
		# if player has completed the level
		if game_over == 1 :
			# reset game and go to next level
			if level > 2 :
				level += 1
				score = 0
			if level < max_levels:
				# reset level
				level += 1
				world_data = []
				world = reset_level(level)
				game_over = 0
				score = 0
			else:
				if restart_button.draw():
					level = 1
					# reset level
					world_data = []
					world = reset_level(level)
					game_over = 0
					score = 0

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()
pygame.quit()

