import pygame
from game import Game


def run_game(game: Game):
    FPS = 60
    clock = pygame.time.Clock()

    while game.running:
        game.event_loop()
        game.update()
        game.draw(game.screen)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    game = Game(allow_keys=True)
    run_game(game)
    pygame.quit()
