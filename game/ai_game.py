import pygame
from .ai_instance import AI_Instance
from typing import List

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


class AI_Game:
    def __init__(self, screen_size, genomes, config):
        self.screen_size = screen_size
        self.screen = pygame.display.set_mode(
            self.screen_size)
        self.screen_rect = self.screen.get_rect()

        self.background = fill_background(self.screen_size)
        self.background_rect = self.background.get_rect()

        self.genomes = genomes
        self.ai_instances: List[AI_Instance] = []
        for genome_id, genome in genomes:
            genome.fitness = 0
            ai_instance = AI_Instance(genome, config, self.screen_rect)
            self.ai_instances.append(ai_instance)

    def update(self):
        for ai_instance in self.ai_instances:
            ai_instance.update()

    def draw(self):
        for ai_instance in self.ai_instances:
            ai_instance.draw()
