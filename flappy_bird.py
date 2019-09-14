from fb_class import *
import pygame

WIN_WIDTH = 500
WIN_HEIGHT = 800
FLOOR = 730
FPS = 15

# Features
HARD_MODE = False

def main():
	"""
	Run the simulation of the current population of birds
	and set their fitness based on the distance they reach
	in the game
	"""
	birds = []
	base = Base(FLOOR)
	pipes = []
	win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
	clock = pygame.time.Clock()

	score = 0

	run = True
	start = lost = False

	while run:
		if HARD_MODE:
			clock.tick(FPS * 2)
		else:
			clock.tick(FPS)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				quit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_s:
					if not start:
						# Reset value and initiate the game
						start = True
						lost = False
						score = 0
						birds.append(Bird(230, 350))

						if HARD_MODE:
							pipes.append(Pipe(random.randrange(450, 600)))
						else:
							pipes.append(Pipe(600))
				elif event.key in [pygame.K_SPACE, pygame.K_UP, pygame.K_RETURN]:
						birds[0].jump()

		pipe_ind = 0
		if start:
			birds[0].move()
			if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
					pipe_ind = 1

			add_pipe = False
			rem = []
			for pipe in pipes:
				for x, bird in enumerate(birds):
					# Check for collision
					if pipe.collide(bird) or bird.y + bird.img.get_height() >= FLOOR or bird.y < 0:
						birds.pop(x)
						start = False
						lost = True

				if not pipe.passed and pipe.x < bird.x:
					pipe.passed = True
					add_pipe = True

				if pipe.x + pipe.PIPE_TOP.get_width() < 0:
					rem.append(pipe)

				pipe.move()

			if add_pipe:
				score += 1
				if HARD_MODE:
					pipes.append(Pipe(random.randrange(450, 600)))
				else:
					pipes.append(Pipe(600))

			for r in rem:
				pipes.remove(r)

			base.move()

		if lost:
			pipes = []

		draw_window(win, birds, pipes, base, score, 1, pipe_ind, start, lost)


if __name__ == "__main__":
	main()
