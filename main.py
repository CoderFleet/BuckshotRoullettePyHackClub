import pygame
import sys
import random

pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Buckshot Roulette")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

FONT = pygame.font.SysFont(None, 55)

NUM_SHELLS = 6
live_shells = 1
player_lives = 2
dealer_lives = 2
player_turn = True
wager = 1

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def draw_game():
    WINDOW.fill(BLACK)
    draw_text("Buckshot Roulette", FONT, WHITE, WINDOW, WINDOW_WIDTH // 2, 50)
    draw_text(f"Player Lives: {player_lives}", FONT, WHITE, WINDOW, WINDOW_WIDTH // 2, 100)
    draw_text(f"Dealer Lives: {dealer_lives}", FONT, WHITE, WINDOW, WINDOW_WIDTH // 2, 150)
    draw_text(f"Wager: {wager}", FONT, WHITE, WINDOW, WINDOW_WIDTH // 2, 200)
    
    pygame.draw.rect(WINDOW, GREEN, pygame.Rect(WINDOW_WIDTH // 2 - 70, WINDOW_HEIGHT // 2 - 70, 140, 140), 2)
    pygame.draw.circle(WINDOW, WHITE, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2), 70, 2)

def initialize_shells():
    shells = [True] * live_shells + [False] * (NUM_SHELLS - live_shells)
    random.shuffle(shells)
    return shells

def main():
    global player_lives, dealer_lives, player_turn, wager
    shells = initialize_shells()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if player_turn:
                        print("Player's turn to shoot.")
                        if shells[0]:
                            dealer_lives -= 1
                            print("Shot! Dealer loses a life.")
                        else:
                            print("Blank! No effect.")
                        player_turn = False
                    else:
                        print("Dealer's turn to shoot.")
                        if shells[0]:
                            player_lives -= 1
                            print("Shot! Player loses a life.")
                        else:
                            print("Blank! No effect.")
                        player_turn = True
                    shells.pop(0)
                    if not shells:
                        shells = initialize_shells()

        draw_game()
        pygame.display.flip()

if __name__ == "__main__":
    main()
