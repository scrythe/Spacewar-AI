from os import path
import neat
from poppulation_game import Population_Game
from time import time
import pygame
import pickle

TOTAL_WIDTH = 1280
TOTAL_HEIGHT = 720
SCREEN_SIZE = TOTAL_WIDTH, TOTAL_HEIGHT


def draw(start_time, time_display_screen, game: Population_Game):
    if time() > start_time + time_display_screen:
        game.draw()
        pygame.display.flip()


def eval_genomes(genomes, config):
    game = Population_Game(genomes, config, SCREEN_SIZE)
    start_time = time()
    start_show_screen_time_after = 0

    run = True
    while run:
        game.run()
        game.update()
        draw(start_time, start_show_screen_time_after, game)
        run = not game.check_game_end()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


def run_neat_population(config):
    # population = neat.Population(config)
    population = neat.Checkpointer.restore_checkpoint('neat-checkpoint-499')
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    population.add_reporter(neat.Checkpointer(1))

    best_genome = population.run(eval_genomes, 500)
    with open('best.pickle', 'wb') as f:
        # save best genome in 'best.pickle' file
        pickle.dump(best_genome, f)


def run_single_genome(config):
    for i in range(3):
        with open('best.pickle', 'rb') as f:
            best_ai = pickle.load(f)
        best_genome = [(0, best_ai)]
        eval_genomes(best_genome, config)
        print(best_genome[0][1].fitness)


if __name__ == '__main__':
    local_dir = path.dirname(__file__)
    config_path = path.join(local_dir, 'config.txt')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    # run_neat_population(config)
    run_single_genome(config)
