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
            reward += width_diffrence / self.screen_rect.width
        return reward

    def draw_line(self, screen: pygame.Surface):
        start_pos = self.player_ship.rect.midtop
        end_pos = self.get_first_enemy().rect.midbottom
        pygame.draw.line(screen, self.color, start_pos, end_pos)

    def evaluate(self):
        frames = self.frames

        # less rewarding the more go
        movement_to_player = self.movement_to_player
        log_content = (movement_to_player / 10) + 1 + (9/10)
        movement_to_reward = (50 * log(log_content, 2) / frames) * 10
        if movement_to_player < 1:
            movement_to_reward = 0

        # first good reward for moving, but gets worse the more done
        movement_away_player = self.movement_away_player
        movement_away_reward = (movement_away_player / frames) * -5

        # no to much standing still when not near enemy
        near_enemy_counter_reward = (self.near_enemy_counter / frames) * 2

        shot_accuracity_reward = self.calculate_distance_reward_shots() * 2

        enemy_distance = self.get_distance_from_enemy()
        width_diffrence = self.screen_rect.width - enemy_distance
        last_point_accuracity_reward = width_diffrence / self.screen_rect.width

        # beginning less reward cause random shots don't matter, but increases exponential
        hits_reward = 0.5 * (1.5 ** self.hits)
        if self.hits > 1:
            hits_reward += 3

        # some reward for being able to shoot
        shots_reward = 2 * self.shots ** 0.1

        # shouldn't switch directions often, but direction change less bad if enemy shot
        direction_changes_reward = (
            self.direction_changes / (self.hits + 1)) * -0.1

        self.genome.fitness += movement_to_reward
        self.genome.fitness += movement_away_reward
        self.genome.fitness += near_enemy_counter_reward
        self.genome.fitness += shot_accuracity_reward
        self.genome.fitness += last_point_accuracity_reward
        self.genome.fitness += hits_reward
        self.genome.fitness += shots_reward
        self.genome.fitness += direction_changes_reward
        self.genome.fitness += 0  # just to set breakpoint

    def draw(self, screen):
        self.player_ship.lasers.draw(screen)
        self.enemies.draw(screen)
        self.player.draw(screen)
        self.draw_line(screen)
