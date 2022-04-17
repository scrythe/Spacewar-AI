import pygame
from game import Game
import neat
import os
import pickle


def run_game():
    FPS = 60
    clock = pygame.time.Clock()
    game = Game(allow_keys=True)

    while game.running:
        game.event_loop()
        game.update()
        game.draw(game.screen)
        game_information = game.get_game_information()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)


def run_neat(config):
    # population = neat.Checkpointer.restore_checkpoint('')
    population = neat.Population(config)  # setup population
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)  # make stats like fitness to be pritten
    population.add_reporter(neat.Checkpointer(1))  # checkpoint every gen

    # run population -> evaluate every genome / get fitness of every genome etc
    # let population run 50 generations and return best one to winner
    winner = population.run(eval_genomes, 1)
    with open('best.pickle', 'wb') as f:
        # save best genome in 'best.pickle' file
        pickle.dump(winner, f)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    run_neat(config)
