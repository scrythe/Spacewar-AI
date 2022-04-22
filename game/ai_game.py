import pygame
from .ai_instance import AI_Instance
from typing import List
from .enemy import Enemy
import random

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

        # coords for enemy, make every enemy have same coords so best ai isn't picked
        # because it was luckier
        random_x_enemies_array = [100, 800, 100, 800, 100, 800]
        enemy_structur = Enemy(pygame.Rect(0, 0, 0, 0), 1, 0)
        for random_x in range(100000):
            max_left = enemy_structur.image.get_width()
            max_right = self.screen_rect.right-enemy_structur.image.get_width()
            random_x = random.randint(max_left, max_right)
            random_x_enemies_array.append(random_x)

        random_x_player = 900
        # random_x_player = random.randint(
        #     self.screen_rect.left, self.screen_rect.right)

        for genome_id, genome in genomes:
            genome.fitness = 0
            ai_instance = AI_Instance(
                genome, config, self.screen_rect, random_x_enemies_array, random_x_player)
            self.ai_instances.append(ai_instance)

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
            ai_instance.evaluate()
            self.ai_instances.pop(ai_instance_index)

    def check_lost(self):
        if len(self.ai_instances) == 0:
            return True
        return False

    def draw(self):
        self.screen.blit(self.background, self.background_rect)
        for ai_instance in self.ai_instances:
            ai_instance.draw(self.screen)
