import pygame
from typing import List
from individual_instance import Individual_Instance
import neat

pygame.init()


def fill_background(screen_size):
    background = pygame.Surface(screen_size)
    background_image = pygame.image.load('assets/background.png').convert()
    background_image_rect = background_image.get_rect()

    background.blit(background_image, background_image_rect.topleft)
    background.blit(background_image, background_image_rect.topright)
    background.blit(background_image, background_image_rect.bottomleft)
    background.blit(background_image, background_image_rect.bottomright)

    return background


def create_and_game_population(genomes, config, screen_rect: pygame.Rect):
    half_screen = screen_rect.width / 2
    first_6_pos = [half_screen - (half_screen / 3), half_screen + (half_screen / 3),
                   half_screen - (half_screen / 2), half_screen + (half_screen / 2), screen_rect.left, screen_rect.right]

    sort_by_worst_fitness(genomes)
    ai_game_population: List[Individual_Instance] = []
    best_genome = determine_best_genome_id(genomes)
    for genome_id, genome in genomes:
        genome: neat.DefaultGenome
        star = genome_id == best_genome
        individual_instance = Individual_Instance(
            genome, config, screen_rect, first_6_pos, star)
        ai_game_population.append(individual_instance)

    return ai_game_population


def sort_by_worst_fitness(genomes):
    for genome_id, genome in genomes:
        if genome.fitness == None:
            genome.fitness = 0

    def key(genome: tuple[int, neat.DefaultGenome]
            ): return genome[1].fitness
    genomes.sort(key=key)  # no reverse because draw worst first


def determine_best_genome_id(genomes):
    # best genome is at bottom
    best_genome: tuple[int, neat.DefaultGenome] = genomes[-1]
    return best_genome[0]


class Population_Game:
    def __init__(self, genomes, config, screen_size):
        self.screen = pygame.display.set_mode(screen_size)
        self.screen_rect = self.screen.get_rect()

        self.background = fill_background(screen_size)
        self.background_rect = self.background.get_rect()

        self.genomes = genomes
        self.ai_game_instances = create_and_game_population(
            genomes, config, self.screen_rect)

    def run(self):
        for individual_instance in self.ai_game_instances:
            individual_instance.run_ai()

    def update(self):
        for index, individual_instance in enumerate(self.ai_game_instances):
            individual_instance.update()
            self.check_if_ai_lost(individual_instance, index)

    def check_if_ai_lost(self, ai_instance: Individual_Instance, ai_instance_index):
        if ai_instance.lost:
            ai_instance.evaluate()
            self.ai_game_instances.pop(ai_instance_index)

    def check_game_end(self):
        if len(self.ai_game_instances) == 0:
            return True
        return False

    def draw(self):
        self.screen.blit(self.background, self.background_rect)
        for individual_instance in self.ai_game_instances:
            individual_instance.draw(self.screen)
