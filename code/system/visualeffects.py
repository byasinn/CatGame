import pygame

def fade(window, fade_in=True, speed=10):
    fade_surface = pygame.Surface(window.get_size()).convert()
    fade_surface.fill((0, 0, 0))
    clock = pygame.time.Clock()

    alpha_range = range(255, -1, -speed) if fade_in else range(0, 256, speed)

    for alpha in alpha_range:
        fade_surface.set_alpha(alpha)
        window.blit(fade_surface, (0, 0))
        pygame.display.flip()
        clock.tick(60)