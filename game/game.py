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
    TOTAL_WIDTH = 1280
    TOTAL_HEIGHT = 720
    SCREEN_SIZE = TOTAL_WIDTH, TOTAL_HEIGHT
    FPS = 60

    def __init__(self):
        self.running = True
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(
            self.SCREEN_SIZE)
        self.screen_rect = self.screen.get_rect()

        self.background = fill_background(self.SCREEN_SIZE)
        self.background_rect = self.background.get_rect()

        ship = Ship(self.screen_rect)
        self.player = pygame.sprite.GroupSingle(ship)
        self.player_ship: Ship = self.player.sprite

        self.enemies = pygame.sprite.Group(Enemy(self.screen_rect))

        self.hits = 0

    def run(self):
        while self.running:
            self.event_loop()
            self.update()
            self.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(self.FPS)

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.player_ship.shoot_laser()

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

    def draw(self, screen: pygame.Surface):
        screen.blit(self.background, self.background_rect)
        self.player_ship.lasers.draw(screen)
        self.enemies.draw(screen)
        self.player.draw(screen)

    def get_first_enemy(self):
        enemy: Enemy = self.enemies.sprites()[0]
        return enemy

    def get_game_information(self):
        ammo = self.player_ship.ammo
        ship_rect = self.player_ship.rect
        enemy_rect = self.get_first_enemy().rect
        game_info = Game_Information(ammo, ship_rect, enemy_rect)
        return game_info


class Game_Information:
    def __init__(self, ammo, ship_rect: pygame.Rect, enemy_rect: pygame.Rect):
        self.ammo = ammo
        self.ship_x = ship_rect.centerx
        self.enemy_x = enemy_rect.centerx
