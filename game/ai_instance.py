from math import log
from random import randint
import neat
import pygame
from .ship import Ship
from .enemy import Enemy
from typing import List


class AI_Instance:
    def __init__(self, genome: neat.DefaultGenome, config, screen_rect: pygame.Rect):
        self.screen_rect = screen_rect
        self.genome = genome
        self.net = neat.nn.FeedForwardNetwork.create(self.genome, config)
        self.player = pygame.sprite.GroupSingle(Ship(self.screen_rect))
        self.player_ship: Ship = self.player.sprite
        self.enemies = pygame.sprite.Group(Enemy(self.screen_rect))
        self.hits = 0
        self.movement_to_player = 0
        self.movement_away_player = 0
        self.shot_distance_from_enemy = []
        self.frames = 0
        self.near_enemy_counter = 0
        self.shots = 0

        self.lives = 8

        self.direction_changes = 0
        self.right = True

        self.lost = False
        self.color = randint(0, 255), randint(0, 255), randint(0, 255)

    def get_first_enemy(self):
        enemies: List[Enemy] = self.enemies.sprites()
        return enemies[0]

    def run_ai(self):
        self.run_decision()

    def run_decision(self):
        inputs = self.player_ship.ammo, self.player_ship.rect.centerx, self.get_first_enemy().rect.centerx
        output = self.net.activate(inputs)
        decision = output.index(max(output))

        if decision == 0:
            if self.player_ship.shoot_laser():
                self.shot_distance_from_enemy.append(
                    self.get_distance_from_enemy())
                self.shots += 1
        if decision == 1:
            self.player_ship.move_right()
            if self.player_ship.rect.centerx < self.get_first_enemy().rect.centerx:
                self.movement_to_player += 1
            else:
                self.movement_away_player += 1
            if not self.right:
                self.direction_changes += 1
        if decision == 2:
            self.player_ship.move_left()
            if self.player_ship.rect.centerx > self.get_first_enemy().rect.centerx:
                self.movement_to_player += 1
            else:
                self.movement_away_player += 1
            if self.right:
                self.direction_changes += 1

        # if 3, then nothing

    def collision(self):
        if pygame.sprite.groupcollide(self.player_ship.lasers, self.enemies, False, False):
            if pygame.sprite.groupcollide(self.player_ship.lasers, self.enemies, True, True, pygame.sprite.collide_mask):
                self.hits += 1
                self.player_ship.ammo += 1
                self.enemies.add(Enemy(self.screen_rect))

    def check_lost(self):
        if self.player_ship.ammo == 0 and len(self.player_ship.lasers) == 0:
            self.lost = True

    def update(self):
        self.player.update()
        self.collision()
        self.check_lost()
        if self.get_first_enemy().enemy_hit():
            self.lives -= 1
            self.enemies.empty()
            self.enemies.add(Enemy(self.screen_rect))
        if self.lives == 0:
            self.lost = True
        self.frames += 1
        self.check_if_near_enemy()

    def check_if_near_enemy(self):
        if self.get_distance_from_enemy() > self.get_first_enemy().rect.width * 1.1:
            self.near_enemy_counter += 1
        else:
            self.near_enemy_counter -= 1

    def get_distance_from_enemy(self):
        distance_diffrence = self.player_ship.rect.centerx - \
            self.get_first_enemy().rect.centerx
        return abs(distance_diffrence)

    def calculate_distance_reward_shots(self):
        reward = 0
        for shot_distance in self.shot_distance_from_enemy:
            width_diffrence = self.screen_rect.width - shot_distance
            # get exponentially worse, the further away the hit is
            reward += (width_diffrence / self.screen_rect.width) ** 1.2
        return reward

    def draw_line(self, screen: pygame.Surface):
        start_pos = self.player_ship.rect.midtop
        end_pos = self.get_first_enemy().rect.midbottom
        pygame.draw.line(screen, self.color, start_pos, end_pos)

    def evaluate(self):
        frames = self.frames

        # less rewarding the more go
        movement_to_per_s = self.movement_to_player / frames
        movement_to_reward = 5 * (movement_to_per_s ** 0.6)
        if self.movement_to_player < 1:
            movement_to_reward = 0

        # first slow but gets more exponential
        movement_away_per_s = self.movement_away_player / frames
        movement_away_reward = 0.25 * (movement_away_per_s ** 1.2)

        # reward movers, but prefer those who don't go too much to other direction
        movement_reward = (movement_to_reward -
                           movement_away_reward) + movement_away_per_s

        # no to much standing still when not near enemy
        near_enemy_counter_reward = 1.4 * \
            (self.near_enemy_counter / frames) ** 1.2
        near_enemy_counter_reward = near_enemy_counter_reward.real  # complex to real

        # exponential (look function)
        shot_accuracity_reward = self.calculate_distance_reward_shots()

        hits_reward = 4 * (self.hits ** 1.5)
        miss_shots_reward = 0.6 * (self.shots ** 1.8)

        # reward shooters, but too many miss shots are bad
        shots_hits_reward = hits_reward - miss_shots_reward

        # shouldn't switch directions often, but direction change less bad if enemy shot
        direction_changes_reward = (
            (self.direction_changes / (self.hits + 1)) ** 1.25 / self.near_enemy_counter) * -0.5

        fitness = 0
        fitness += movement_reward + near_enemy_counter_reward + shot_accuracity_reward
        fitness += shots_hits_reward + direction_changes_reward

        self.genome.fitness = fitness

    def draw(self, screen):
        self.player_ship.lasers.draw(screen)
        self.enemies.draw(screen)
        self.player.draw(screen)
        self.draw_line(screen)
