
from fb_class import Bird, Base, Pipe, draw_window
import os
import neat
import math
import pickle
import random
import pygame

WIN_WIDTH = 500
WIN_HEIGHT = 800
FLOOR = 730
GEN = 0

# Features
CHECKPOINT = False
NUM_CHECKPOINT = 2
BREAK_SCORE = 50
FPS = 120


# Main program code
def main(genomes, config, break_score=True):
	"""
	Run the simulation of the current population of birds
	and set their fitness based on the distance they reach
	in the game
	:param genomes: list of genomes
	:param config: config files for NEAT neural network
	:param break_score: break game at BREAK_SCORE (default to True)
	"""
	global GEN
	GEN += 1

	# Create  lists holiding the genome itself,
	# the neural network associated with the genome
	# and the bird object that uses the network to play
	nets = []
	ge = []
	birds = []

	for g_id, g in genomes:
		net = neat.nn.FeedForwardNetwork.create(g, config)
		nets.append(net)
		birds.append(Bird(230, 350))
		g.fitness = 0
		ge.append(g)

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

		pipe_ind = 0
		if len(birds) > 0:
			# Determine whether to use the first or second pipe on the screen
			# for neural network input
			if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
				pipe_ind = 1

		for x, bird in enumerate(birds):
			# Give each bird a fitness of 0.1 for each frame it stays alive
			ge[x].fitness += 0.1
			bird.move()

			# Send bird location, top pipe location and bottom pipe location
			# and determine from network whether to jump or not
			output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

			# Use tanh as activation function
			# Result will in the range [-1, 1]
			# Jump if result > 0.5
			if output[0] > 0.5:
				bird.jump()

		add_pipe = False
		rem = []
		for pipe in pipes:
			for x, bird in enumerate(birds):
				# Check for collision
				if pipe.collide(bird):
					# Reduce fitness for bird who collides
					# such that bird that flew far but collides always
					# aren't favored
					ge[x].fitness -= 1
					birds.pop(x)
					nets.pop(x)
					ge.pop(x)

			if not pipe.passed and pipe.x < bird.x:
				pipe.passed = True
				add_pipe = True

			if pipe.x + pipe.PIPE_TOP.get_width() < 0:
				rem.append(pipe)

			pipe.move()

		if add_pipe:
			score += 1
			for g in ge:
				g.fitness += 5
			pipes.append(Pipe(random.randrange(450, 600)))

		for r in rem:
			pipes.remove(r)

		for x, bird in enumerate(birds):
			if bird.y + bird.img.get_height() >= FLOOR or bird.y < 0:
				birds.pop(x)
				nets.pop(x)
				ge.pop(x)

		base.move()
		draw_window(win, birds, pipes, base, score, GEN, pipe_ind)

		# Break game if score gets large enough
		if break_score:
			if score > BREAK_SCORE:
				break


def run(config_path):
	"""
	Runs NEAT algorithm to train a neural network to play flappy bird
	:param config_path: location of config file
	:return: None
	"""
	# Load configuration
	config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

	# Create population, which is the top-level object for NEAT run
	p = neat.Population(config)

	# Add a stdout reporter to show progress in terminal
	p.add_reporter(neat.StdOutReporter(True))
	stats = neat.StatisticsReporter()
	p.add_reporter(stats)
	if CHECKPOINT:
		p.add_reporter(neat.Checkpointer(NUM_CHECKPOINT))

	# Run for up to 50 generations
	winner = p.run(main, 50)

	# Show final stats
	print('\nBest genome:\n{!s}'.format(winner))

	# Save winner genome using pickle
	with open("winner-genome.pickle", "wb") as f:
		pickle.dump(winner, f, pickle.HIGHEST_PROTOCOL)

	# If checkpoint is enabled,
	if CHECKPOINT:
		if GEN > NUM_CHECKPOINT:
			last_save = math.floor((GEN - 1) / NUM_CHECKPOINT) * NUM_CHECKPOINT - 1
			f_name = 'neat-checkpoint-' + str(last_save)
			p = neat.Checkpointer.restore_checkpoint(f_name)
			p.add_reporter(neat.StdOutReporter(True))
			stats = neat.StatisticsReporter()
			p.add_reporter(stats)

			winner = p.run(main, 50)
			with open("winner-genome.pickle", "wb") as f:
				pickle.dump(winner, f, pickle.HIGHEST_PROTOCOL)

			print('\nBest genome:\n{!s}'.format(winner))


def winner_run(config_path, winner_genome_path):
	"""
	Runs the game using the flappy bird with winning network
	:param config_path: location of config file
	:param winner_genome_path: location of the winner genome
	:return: None
	"""
	# Load configuration
	with open(winner_genome_path, 'rb') as f:
		winner_g = pickle.load(f)

	config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

	print('\nWinner from NEAT: Final Run\n')
	main(enumerate([winner_g]), config, False)

	print('\nBest genome:\n{!s}'.format(winner_g))


if __name__ == "__main__":
	# Determine path to configuration file.
	# This path manipulation is here so that the script will run
	# successfully regardless of the current working directory
	local_dir = os.path.dirname(__file__)
	config_path = os.path.join(local_dir, "config-feedforward.txt")
	winner_genome_path = os.path.join(local_dir, "winner-genome.pickle")
	run(config_path)
	winner_run(config_path, winner_genome_path)
