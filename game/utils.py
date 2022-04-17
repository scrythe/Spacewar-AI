import pygame


def scale_image(image: pygame.Surface, factor):
    size = round(image.get_width() *
                 factor), round(image.get_height() * factor)
    return pygame.transform.scale(image, size)
