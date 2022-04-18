import pygame
from .ship import Ship
from .enemy import Enemy

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


class Game:
    def __init__(self, screen_size, allow_keys=True):
        self.allow_keys = allow_keys
        self.running = True
        # self.clock = pygame.time.Clock()
        self.screen_size = screen_size
        self.screen = pygame.display.set_mode(
            self.screen_size)
        self.screen_rect = self.screen.get_rect()

        self.background = fill_background(self.screen_size)
        self.background_rect = self.background.get_rect()

        ship = Ship(self.screen_rect, self.allow_keys)
        self.player = pygame.sprite.GroupSingle(ship)
        self.player_ship: Ship = self.player.sprite

        self.enemies = pygame.sprite.Group(Enemy(self.screen_rect))

        self.hits = 0
        self.amount_shot = 0
        self.shot_distance_from_hits = []
        self.movement_to_player = 0

    # def run(self):
    #     while self.running:
    #         self.event_loop()
    #         self.update()
    #         self.draw(self.screen)
    #         pygame.display.flip()
    #         self.clock.tick(self.FPS)

    def get_distance_from_enemy(self):
        distance_diffrence = self.player_ship.rect.centerx - \
            self.get_first_enemy().rect.centerx
        return abs(distance_diffrence)

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if self.allow_keys:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.player_ship.shoot_laser()

    def ship_shoot_laser(self):
        if self.player_ship.shoot_laser():
            self.amount_shot += 1
            self.shot_distance_from_hits.append(self.get_distance_from_enemy())

    def move_ship_right(self):
        self.player_ship.move_right()
        if self.player_ship.rect.centerx < self.get_first_enemy().rect.centerx:
            self.movement_to_player += 1
        self.movement_to_player -= 1.005

    def move_ship_left(self):
        self.player_ship.move_left()
        if self.player_ship.rect.centerx > self.get_first_enemy().rect.centerx:
            self.movement_to_player += 1
        else:
            self.movement_to_player -= 1.005

    def collision(self):
        if pygame.sprite.groupcollide(self.player_ship.lasers, self.enemies, False, False):
            if pygame.sprite.groupcollide(self.player_ship.lasers, self.enemies, True, True, pygame.sprite.collide_mask):
                self.hits += 1
                self.player_ship.ammo += 1
                self.enemies.add(Enemy(self.screen_rect))

    def check_lost(self):
        if self.player_ship.ammo == 0 and len(self.player_ship.lasers) == 0:
            self.running = False

    def update(self):
        self.player.update()
        self.collision()
        self.check_lost()
        if self.get_first_enemy().enemy_hit():
            self.running = False

    def draw(self, screen: pygame.Surface):
        screen.blit(self.background, self.background_rect)
        self.player_ship.lasers.draw(screen)
        self.enemies.draw(screen)
        self.player.draw(screen)

    def get_first_enemy(self):
        enemy: Enemy = self.enemies.sprites()[0]
        return enemy

    def distance_between_enemy(self):
        self.player_ship.lasers

    def get_game_information(self):
        ammo = self.player_ship.ammo
        ship_rect = self.player_ship.rect
        enemy_rect = self.get_first_enemy().rect
        hits = self.hits
        shot_distance_from_hits = self.shot_distance_from_hits
        amount_shot = self.amount_shot
        distance_from_enemy = self.get_distance_from_enemy()
        total_movement_to_player = self.movement_to_player
        game_info = Game_Information(
            ammo, ship_rect, enemy_rect, hits, shot_distance_from_hits, amount_shot, distance_from_enemy, total_movement_to_player)
        return game_info


class Game_Information:
    def __init__(self, ammo, ship_rect: pygame.Rect, enemy_rect: pygame.Rect, hits, shot_distance_from_hits, amount_shot, distance_from_enemy, total_movement_to_player):
        self.ammo = ammo
        self.ship_x = ship_rect.centerx
        self.enemy_x = enemy_rect.centerx
        self.hits = hits
        self.shot_distance_from_hits = shot_distance_from_hits
        self.amount_shot = amount_shot
        self.distance_from_enemy = distance_from_enemy
        self.total_movement_to_player = total_movement_to_player
