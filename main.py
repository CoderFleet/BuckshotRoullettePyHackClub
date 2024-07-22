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
SMALL_FONT = pygame.font.SysFont(None, 35)

NUM_SHELLS = 6
live_shells = 1
player_lives = 2
dealer_lives = 2
player_turn = True
wager = 1
game_over = False

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

    if game_over:
        draw_text("Game Over!", FONT, RED, WINDOW, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
    elif player_turn:
        draw_text("Player's Turn", SMALL_FONT, GREEN, WINDOW, WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50)
    else:
        draw_text("Dealer's Turn", SMALL_FONT, RED, WINDOW, WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50)

def initialize_shells():
    shells = [True] * live_shells + [False] * (NUM_SHELLS - live_shells)
    random.shuffle(shells)
    return shells

def reset_game():
    global shells, player_lives, dealer_lives, player_turn, wager, live_shells, game_over
    shells = initialize_shells()
    player_lives = 2
    dealer_lives = 2
    player_turn = True
    wager = 1
    live_shells = 1
    game_over = False

def handle_wager():
    global wager
    wager = min(wager + 1, 3)

def handle_turn():
    global player_lives, dealer_lives, player_turn, game_over, shells
    if player_turn:
        if shells[0]:
            dealer_lives -= wager
            if dealer_lives <= 0:
                print("Player wins!")
                game_over = True
        else:
            print("Blank! No effect.")
            handle_wager()
        player_turn = False
    else:
        if shells[0]:
            player_lives -= wager
            if player_lives <= 0:
                print("Dealer wins!")
                game_over = True
        else:
            print("Blank! No effect.")
            handle_wager()
        player_turn = True
    shells.pop(0)
    if not shells:
        shells = initialize_shells()

def main():
    global player_lives, dealer_lives, player_turn, wager, game_over
    reset_game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    print(f"{'Player' if player_turn else 'Dealer'} pulls the trigger.")
                    handle_turn()
                if event.key == pygame.K_r:
                    print("Resetting game.")
                    reset_game()

        draw_game()
        pygame.display.flip()

if __name__ == "__main__":
    main()
