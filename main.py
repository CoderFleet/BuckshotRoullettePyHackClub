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
round_number = 1
ITEMS = {
    "magnifying_glass": False,
    "cigarette_pack": False,
    "beer_can": False,
    "handsaw": False,
    "handcuffs": False
}
sudden_death_mode = False

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
    draw_text(f"Round: {round_number}", FONT, WHITE, WINDOW, WINDOW_WIDTH // 2, 250)

    pygame.draw.rect(WINDOW, GREEN, pygame.Rect(WINDOW_WIDTH // 2 - 70, WINDOW_HEIGHT // 2 - 70, 140, 140), 2)
    pygame.draw.circle(WINDOW, WHITE, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2), 70, 2)

    if game_over:
        draw_text("Game Over!", FONT, RED, WINDOW, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
    elif player_turn:
        draw_text("Player's Turn", SMALL_FONT, GREEN, WINDOW, WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50)
    else:
        draw_text("Dealer's Turn", SMALL_FONT, RED, WINDOW, WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50)

    draw_items()

def draw_items():
    x, y = 50, WINDOW_HEIGHT - 100
    for item, active in ITEMS.items():
        if active:
            draw_text(item.replace('_', ' ').title(), SMALL_FONT, BLUE, WINDOW, x, y)
            x += 150

def initialize_shells():
    shells = [True] * live_shells + [False] * (NUM_SHELLS - live_shells)
    random.shuffle(shells)
    return shells

def reset_game():
    global shells, player_lives, dealer_lives, player_turn, wager, live_shells, game_over, round_number, ITEMS, sudden_death_mode
    shells = initialize_shells()
    player_lives = 2
    dealer_lives = 2
    player_turn = True
    wager = 1
    live_shells = 1
    game_over = False
    round_number = 1
    ITEMS = {key: False for key in ITEMS}
    sudden_death_mode = False

def handle_wager():
    global wager
    wager = min(wager + 1, 3)

def handle_turn():
    global player_lives, dealer_lives, player_turn, game_over, shells, ITEMS, sudden_death_mode
    if player_turn:
        if ITEMS["magnifying_glass"]:
            print("Magnifying Glass: Checking shell...")
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
        if ITEMS["beer_can"]:
            print("Beer Can: Skipping turn...")
            player_turn = True
        elif ITEMS["handsaw"]:
            print("Handsaw: Double damage!")
            if shells[0]:
                player_lives -= 2 * wager
                if player_lives <= 0:
                    print("Dealer wins!")
                    game_over = True
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

def distribute_items():
    global ITEMS
    possible_items = list(ITEMS.keys())
    num_items = 2 if round_number == 2 else 4
    items_to_distribute = random.sample(possible_items, num_items)
    ITEMS = {item: True for item in items_to_distribute}

def handle_sudden_death():
    global game_over, player_lives, dealer_lives
    if player_lives <= 2 or dealer_lives <= 2:
        sudden_death_mode = True
        print("Sudden Death Mode Activated!")
        if player_lives <= 2:
            game_over = True
            print("Player loses in Sudden Death!")
        if dealer_lives <= 2:
            game_over = True
            print("Dealer loses in Sudden Death!")

def main():
    global player_lives, dealer_lives, player_turn, wager, game_over, round_number, sudden_death_mode
    reset_game()
    distribute_items()

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
                    distribute_items()
                if event.key == pygame.K_n:
                    print("Next Round!")
                    round_number += 1
                    if round_number == 3:
                        handle_sudden_death()
                    if round_number <= 3:
                        distribute_items()
                    else:
                        print("Game Over!")
                        game_over = True

        draw_game()
        pygame.display.flip()

if __name__ == "__main__":
    main()
