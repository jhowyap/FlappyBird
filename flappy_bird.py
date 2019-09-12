from fb_class import *
import pygame

WIN_WIDTH = 500
WIN_HEIGHT = 800
FLOOR = 730
FPS = 15


def main():
	"""
	Run the simulation of the current population of birds
	and set their fitness based on the distance they reach
	in the game
	"""
	birds = [Bird(230, 350)]
	base = Base(FLOOR)
	pipes = [Pipe(random.randrange(450, 600))]
	win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
	clock = pygame.time.Clock()

	score = 0

	run = True
	while run and len(birds) > 0:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				quit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					birds[0].jump()

		pipe_ind = 0
		birds[0].move()
		if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
				pipe_ind = 1

		add_pipe = False
		rem = []
		for pipe in pipes:
			for x, bird in enumerate(birds):
				# Check for collision
				if pipe.collide(bird) or bird.y + bird.img.get_height() >= FLOOR or bird.y < 0:
					# birds.pop(x)
					# run = False
					pass

			if not pipe.passed and pipe.x < bird.x:
				pipe.passed = True
				add_pipe = True

			if pipe.x + pipe.PIPE_TOP.get_width() < 0:
				rem.append(pipe)

			pipe.move()

		if add_pipe:
			score += 1
			pipes.append(Pipe(random.randrange(450, 600)))

		for r in rem:
			pipes.remove(r)

		base.move()
		draw_window(win, birds, pipes, base, score, 1, pipe_ind)

	run = True
	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				quit()

		show_final_score(win, score)


if __name__ == "__main__":
	main()
