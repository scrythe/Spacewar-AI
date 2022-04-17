import pygame
from ship import Ship


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

        self.ship = Ship(self.screen_rect)
        self.player = pygame.sprite.GroupSingle(self.ship)

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

    def update(self):
        self.player.update()

    def draw(self, screen: pygame.Surface):
        screen.blit(self.background, self.background_rect)
        self.player.draw(screen)


if __name__ == '__main__':
    pygame.init()
    game = Game()
    game.run()
    pygame.quit()
