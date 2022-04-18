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

        self.running = True

    def run_ais(self):
        for ai_instace in self.ai_instances:
            ai_instace.run_ai()

    def update(self):
        for ai_instance in self.ai_instances:
            ai_instance.update()
            self.check_lost_ai(ai_instance)

    def check_lost_ai(self, ai_instance: AI_Instance):
        if ai_instance.lost:
            ai_instance_index = self.ai_instances.index(ai_instance)
            self.ai_instances.pop(ai_instance_index)

    def check_lost(self):
        if len(self.ai_instances) == 0:
            self.running = False

    def draw(self):
        self.screen.blit(self.background, self.background_rect)
        for ai_instance in self.ai_instances:
            ai_instance.draw(self.screen)
