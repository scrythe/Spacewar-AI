import pygame
from game import Game
import neat
import os
import pickle
import time

TOTAL_WIDTH = 1280
TOTAL_HEIGHT = 720
SCREEN_SIZE = TOTAL_WIDTH, TOTAL_HEIGHT


def calculate_distance_reward(distances):
    reward = 0
    for distances in distances:
        width_diffrence = TOTAL_WIDTH-distances
        reward += width_diffrence/TOTAL_WIDTH
    return reward


def run_game():
    FPS = 60
    clock = pygame.time.Clock()
    game = Game(SCREEN_SIZE, allow_keys=True)

    while game.running:
        game.event_loop()
        game.update()
        game.draw(game.screen)
        game_information = game.get_game_information()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


def run_ai_game(net: neat.nn.FeedForwardNetwork):
    game = Game(SCREEN_SIZE, allow_keys=False)
    fitness = 0
    start_time = time.time()
    MAX_TIME = 4

    run = True
    while game.running:
        game.event_loop()
        game_information = game.get_game_information()

        output = net.activate(
            (game_information.ammo, game_information.ship_x, game_information.enemy_x))
        decision = output.index(max(output))

        if decision == 0:
            game.ship_shoot_laser()
        if decision == 1:
            game.move_ship_right()
        if decision == 2:
            game.move_ship_left()
        # if 3, then nothing

        game.update()

        if start_time + MAX_TIME <= time.time():
            game.running = False

        if not game.running:
            fitness += calculate_distance_reward(
                game_information.shot_distance_from_hits)
            fitness += game_information.hits
            fitness += game_information.amount_shot / 2
            return fitness

        game.draw(game.screen)
        pygame.display.flip()


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        genome.fitness = run_ai_game(net)


def run_neat(config):
    # population = neat.Checkpointer.restore_checkpoint('')
    population = neat.Population(config)  # setup population
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)  # make stats like fitness to be pritten
    population.add_reporter(neat.Checkpointer(1))  # checkpoint every gen

    # run population -> evaluate every genome / get fitness of every genome etc
    # let population run 50 generations and return best one to winner
    winner = population.run(eval_genomes, 50)
    with open('best.pickle', 'wb') as f:
        # save best genome in 'best.pickle' file
        pickle.dump(winner, f)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    run_neat(config)
