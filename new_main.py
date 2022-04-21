import pygame
from game import AI_Game
import os
import neat
from sys import exit
import pickle

from main import eval_genomes


TOTAL_WIDTH = 1280
TOTAL_HEIGHT = 720
SCREEN_SIZE = TOTAL_WIDTH, TOTAL_HEIGHT


def eval_genomes(genomes, config):
    ai_game = AI_Game(SCREEN_SIZE, genomes, config)

    run = True
    while run:

        ai_game.run_ais()
        run = not ai_game.check_lost()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        ai_game.update()
        ai_game.draw()
        pygame.display.flip()


def run_neat(config):
    # population = neat.Checkpointer.restore_checkpoint('neat-checkpoint-38')
    population = neat.Population(config)  # setup population
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)  # make stats like fitness to be pritten
    population.add_reporter(neat.Checkpointer(1))  # checkpoint every gen

    # run population -> evaluate every genome / get fitness of every genome etc
    # let population run 50 generations
    winner = population.run(eval_genomes, 200)
    with open('best.pickle', 'wb') as f:
        # save best genome in 'best.pickle' file
        pickle.dump(winner, f)


def run_one_neat(config):
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)
    genomes = [(0, winner), (1, winner), (2, winner)]
    eval_genomes(genomes, config)
    for genome_id, genome in genomes:
        print(genome.fitness)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    run_neat(config)
    # run_one_neat(config)
