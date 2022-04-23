from random import randint
import pygame
import neat
from ship import Ship
from random import randint
from enemy import Enemy
from typing import List
from fitness_function import fitness_function


def make_create_random_x_coord_func(screen_rect: pygame.Surface):
    enemy_structur = Enemy(0, pygame.Rect(0, 0, 0, 0), 1)
    max_left = enemy_structur.image.get_width()
    max_right = screen_rect.right-enemy_structur.image.get_width()

    def create_random_x_coord():
        return randint(max_left, max_right)

    return create_random_x_coord


class Individual_Instance:
    MAX_LIVES = 2

    def __init__(self, genome: neat.DefaultGenome, config, screen_rect: pygame.Rect):
        self.genome = genome
        self.net = neat.nn.FeedForwardNetwork.create(self.genome, config)
        self.screen_rect = screen_rect
        self.create_random_x_coord = make_create_random_x_coord_func(
            self.screen_rect)
        self.player = pygame.sprite.GroupSingle(
            Ship(self.screen_rect, self.create_random_x_coord()))
        self.player_ship: Ship = self.player.sprite

        self.x_coord = randint(self.screen_rect.left, self.screen_rect.right)
        self.enemies = pygame.sprite.Group()
        self.add_enemy()

        self.movement_to_player = 0
        self.total_movement = 0
        self.bullet_shots = []
        self.frames = 0
        self.hits = 0
        self.shots = 0

        self.lives = self.MAX_LIVES
        self.lost = False
        self.color = randint(0, 255), randint(0, 255), randint(0, 255)

    def get_first_enemy(self):
        enemies: List[Enemy] = self.enemies.sprites()
        return enemies[0]

    def check_move_to_enemy(self):
        return self.get_first_enemy().rect.centerx - self.player_ship.rect.centerx

    def run_ai(self):
        ammo = self.player_ship.ammo
        player_x = self.player_ship.rect.centerx
        enemy_x = self.get_first_enemy().rect.centerx
        laser_amount = len(self.player_ship.lasers)

        inputs = ammo, player_x, enemy_x, laser_amount
        shoot, move_direction = self.net.activate(inputs)

        if shoot > 0:
            if self.player_ship.shoot_laser(self.frames):
                self.shots += 1
                self.bullet_shots.append(self.get_distance_from_enemy())
        if move_direction > 0:
            self.player_ship.move_right()
            self.total_movement += self.player_ship.SPEED
            if 0 < self.check_move_to_enemy():
                self.movement_to_player += self.player_ship.SPEED

        if move_direction < 0:
            self.player_ship.move_left()
            self.total_movement += self.player_ship.SPEED
            if 0 > self.check_move_to_enemy():
                self.movement_to_player += self.player_ship.SPEED

    def get_distance_from_enemy(self):
        player_x = self.player_ship.rect.centerx
        enemy_x = self.get_first_enemy().rect.centerx
        x_diffrence = player_x - enemy_x
        return abs(x_diffrence)

    def add_enemy(self):
        new_enemy = Enemy(self.create_random_x_coord(),
                          self.screen_rect, self.player_ship.SPEED)
        self.enemies.add(new_enemy)

    def collision(self):
        check_collision = pygame.sprite.groupcollide(
            self.player_ship.lasers, self.enemies, False, False, pygame.sprite.collide_mask)
        if check_collision:
            self.hits += 1
            self.player_ship.ammo += 1
            self.add_enemy()

    def check_lost(self):
        no_ammo = self.player_ship.ammo == 0
        no_lasers = len(self.player_ship.lasers) < 1
        no_lives = self.lives == 0
        if no_ammo and no_lasers or no_lives:
            self.lost = True

    def evaluate(self):
        fitness = fitness_function(self.movement_to_player, self.total_movement,
                                   self.screen_rect.width, self.bullet_shots, self.hits, self.shots, self.frames)
        self.genome.fitness = fitness

    def reduce_live(self):
        self.lives -= 1
        self.enemies.empty()
        self.add_enemy()

    def update(self):
        self.frames += 1
        self.player.update()
        self.collision()
        if self.get_first_enemy().enemy_hit(self.frames):
            self.reduce_live()
        self.check_lost()

    def draw(self, screen: pygame.Surface):
        self.player_ship.lasers.draw(screen)
        self.enemies.draw(screen)
        self.player.draw(screen)
        self.draw_line(screen)

    def draw_line(self, screen: pygame.Surface):
        start_pos = self.player_ship.rect.midtop
        end_pos = self.get_first_enemy().rect.midbottom
        pygame.draw.line(screen, self.color, start_pos, end_pos)
