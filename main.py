import pygame
import sys

pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Buckshot Roulette")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

def draw_title():
    font = pygame.font.SysFont(None, 55)
    text = font.render('Buckshot Roulette', True, WHITE)
    WINDOW.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, 20))

def transition_background():
    r = 0
    g = 0
    b = 0
    while r < 255:
        r += 1
        WINDOW.fill((r, g, b))
        draw_title()
        pygame.display.flip()
        pygame.time.delay(10)
    
    while g < 255:
        g += 1
        WINDOW.fill((r, g, b))
        draw_title()
        pygame.display.flip()
        pygame.time.delay(10)
    
    while b < 255:
        b += 1
        WINDOW.fill((r, g, b))
        draw_title()
        pygame.display.flip()
        pygame.time.delay(10)

def main():
    transition_background()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        WINDOW.fill(BLACK)
        draw_title()
        pygame.display.flip()

if __name__ == "__main__":
    main()
