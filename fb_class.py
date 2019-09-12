import pygame
import os
import random
pygame.font.init()  # init font

# Features
DRAW_LINES = True

# Output attribute (Font, color)
STAT_FONT = pygame.font.SysFont("comicsans", 50)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)

# Images path
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(
	pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(
	pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(
	pygame.image.load(os.path.join("imgs", "bg.png")))


class Bird:
	"""
	Bird class representing the flappy bird
	"""
	IMGS = BIRD_IMGS
	MAX_ROTATION = 25
	ROT_VEL = 20
	ANIMATION_TIME = 5

	def __init__(self, x, y):
		"""
		Initialize the Bird object
		:param x: starting x position (int)
		:param y: starting y position (int)
		:return: None
		"""
		self.x = x
		self.y = y
		self.tilt = 0
		self.tick_count = 0
		self.vel = 0
		self.height = self.y
		self.img_count = 0
		self.img = self.IMGS[0]

	def jump(self):
		"""
		Make the bird jump
		:return: None
		"""
		self.vel = -10.5
		self.tick_count = 0
		self.height = self.y

	def move(self):
		"""
		Make the bird move
		:return: None
		"""
		self.tick_count += 1

		# For downward acceleration
		d = self.vel * self.tick_count + 1.5 * self.tick_count**2

		# Terminal velocity
		if d >= 16:
			d = 16

		if d < 0:
			d -= 2

		self.y = self.y + d

		if (d < 0) or (self.y < self.height + 50):  # tilt up
			if self.tilt < self.MAX_ROTATION:
				self.tilt = self.MAX_ROTATION
		else:  # tilt down
			if self.tilt > -90:
				self.tilt -= self.ROT_VEL

	def draw(self, win):
		"""
		Draw the bird
		:param win: pygame window or surface
		:return: None
		"""
		self.img_count += 1

		# Loop through 3 images for animation of bird
		if self.img_count < self.ANIMATION_TIME:
			self.img = self.IMGS[0]
		elif self.img_count < self.ANIMATION_TIME * 2:
			self.img = self.IMGS[1]
		elif self.img_count < self.ANIMATION_TIME * 3:
			self.img = self.IMGS[2]
		elif self.img_count < self.ANIMATION_TIME * 4:
			self.img = self.IMGS[1]
		elif self.img_count == self.ANIMATION_TIME * 4 + 1:
			self.img = self.IMGS[0]
			self.img_count = 0

		# Show that the bird is not flapping when nose diving
		if self.tilt <= -80:
			self.img = self.IMGS[1]
			self.img_count = self.ANIMATION_TIME * 2

		# Tilt the bird
		rotated_image = pygame.transform.rotate(self.img, self.tilt)
		new_rect = rotated_image.get_rect(
			center=self.img.get_rect(topleft=(self.x, self.y)).center)

		win.blit(rotated_image, new_rect.topleft)

	def get_mask(self):
		"""
		Get the mask fro the current image of the bird
		:return: Mask
		"""
		return pygame.mask.from_surface(self.img)


class Pipe:
	"""
	Pipe class representing the pipe obstacles
	"""
	GAP = 200
	VEL = 5

	def __init__(self, x):
		"""
		Initialize the Pipe object
		:param x: x position of the pipe (int)
		:return: None
		"""
		self.x = x
		self.height = 0

		# The position for the top and bottom of the pipe
		self.top = 0
		self.bottom = 0
		self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
		self.PIPE_BOTTOM = PIPE_IMG

		self.passed = False
		self.set_height()

	def set_height(self):
		"""
		Set the height of the pipe from the top of the screen
		:return: None
		"""
		self.height = random.randrange(50, 450)
		self.top = self.height - self.PIPE_TOP.get_height()
		self.bottom = self.height + self.GAP

	def move(self):
		"""
		Move the pipe
		:return: None
		"""
		self.x -= self.VEL

	def draw(self, win):
		"""
		Draw both the top and bottom of the pipes
		:param win: pygame window or surface
		:return: None
		"""
		win.blit(self.PIPE_TOP, (self.x, self.top))
		win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

	def collide(self, bird):
		"""
		Returns if the bird collides with any of the pipes
		:param bird: Bird object
		:return: Bool
		"""
		bird_mask = bird.get_mask()
		top_mask = pygame.mask.from_surface(self.PIPE_TOP)
		bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

		top_offset = (self.x - bird.x, self.top - round(bird.y))
		bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

		b_point = bird_mask.overlap(bottom_mask, bottom_offset)
		t_point = bird_mask.overlap(top_mask, top_offset)

		if t_point or b_point:
			return True

		return False


class Base:
	"""
	Base class representing the moving floor of the game
	"""
	VEL = 5
	WIDTH = BASE_IMG.get_width()
	IMG = BASE_IMG

	def __init__(self, y):
		"""
		Initialize the Base object
		:param y: y position of the base (int)
		:return: None
		"""
		self.y = y
		self.x1 = 0
		self.x2 = self.WIDTH

	def move(self):
		"""
		Move floor so it looks like scrolling
		:return: None
		"""
		self.x1 -= self.VEL
		self.x2 -= self.VEL

		if self.x1 + self.WIDTH < 0:
			self.x1 = self.x2 + self.WIDTH

		if self.x2 + self.WIDTH < 0:
			self.x2 = self.x1 + self.WIDTH

	def draw(self, win):
		"""
		Draw the floor, showing two images that move together
		:param win: pygame window or surface
		:return: None
		"""
		win.blit(self.IMG, (self.x1, self.y))
		win.blit(self.IMG, (self.x2, self.y))


def draw_window(win, birds, pipes, base, score, gen, pipe_ind):
	"""
	Draws the windows for the main game loop
	:param win: pygame window or surface
	:param birds: list of Bird objects
	:param pipes: list of Pipe objects
	:param base: Base object
	:param score: score of the game (int)
	:param gen: current generation (int)
	:param pipe_ind: index of the closest pipe
	:return: None
	"""
	win.blit(BG_IMG, (0, 0))

	# Draw pipes
	for pipe in pipes:
		pipe.draw(win)

	# Draw base
	base.draw(win)

	for bird in birds:
		# Draw lines from bird to pipes
		if DRAW_LINES:
			try:
				bird_center = (bird.x + bird.img.get_width() / 2, bird.y + bird.img.get_height() / 2)
				pygame.draw.line(win, COLOR_RED, bird_center, (pipes[pipe_ind].x + pipes[pipe_ind].PIPE_TOP.get_width() / 2, pipes[pipe_ind].height), 5)
				pygame.draw.line(win, COLOR_RED, bird_center, (pipes[pipe_ind].x + pipes[pipe_ind].PIPE_BOTTOM.get_width() / 2, pipes[pipe_ind].bottom), 5)
			except:
				pass
		# Draw bird
		bird.draw(win)

	# Score label
	text = STAT_FONT.render("Score: " + str(score), 1, COLOR_WHITE)
	win.blit(text, (win.get_width() - 10 - text.get_width(), 10))

	# Generation label
	text = STAT_FONT.render("Gen: " + str(gen), 1, COLOR_WHITE)
	win.blit(text, (10, 10))

	# Number of birds alive
	text = STAT_FONT.render("Alive: " + str(len(birds)), 1, COLOR_WHITE)
	win.blit(text, (10, 50))

	pygame.display.update()


def show_final_score(win, score):
	win.blit(BG_IMG, (0, 0))

	text = STAT_FONT.render("The bird crashed!", 1, COLOR_WHITE)
	text2 = STAT_FONT.render("You score " + str(score), 1, COLOR_WHITE)

	win.blit(text, ((win.get_width() - text.get_width()) / 2, win.get_height() / 2))
	win.blit(text2, ((win.get_width() - text2.get_width()) / 2, win.get_height() / 2 + text.get_height()))

	pygame.display.update()
