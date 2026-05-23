# ==============================
# Tudurachi Calin Emanuel - 2026
# ==============================

import pygame
import random
import sys

# ========================================================
# CONFIGURATION & ACCESSIBILITY SETTINGS - CAN BE MODIFIED
# ========================================================

# game logic
random_int = random.randint(0, 11)
array = ["COMUNISM", "RĂZBOI", "LIBERTATE", "REVOLUȚIE", "DEMOCRAȚIE", "DICTATURĂ", "PROTEST", "VICTORIE", "OPRESIUNE", "LIBERAȚIE", "CENZURĂ", "REZISTENȚĂ"]

TARGET_WORD = array[random_int]  # randomly selects a word from the list for each game session. You can modify this list to include any words you'd like to use in the game.
GAME_SPEED = 8          # lower = slower/easier. higher = faster/harder.

# grid & sizing
CELL_SIZE = 40          # Size of each square on the screen
GRID_WIDTH = 20         # Number of columns
GRID_HEIGHT = 15        

# colors (RGB Format)
BG_COLOR = (30, 30, 30)         # dark grey background reduces eye strain
GRID_COLOR = (50, 50, 50)       # subtle grid lines help with visual alignment
SNAKE_HEAD_COLOR = (0, 255, 0)  # bright Green
SNAKE_BODY_COLOR = (0, 200, 0)  # slightly darker green
LETTER_COLOR = (255, 255, 0)    # bright Yellow text for maximum contrast
UI_TEXT_COLOR = (255, 255, 255) # white for victory/loss messages

# =============================================================================
# GAME SETUP & INITIALIZATION - DO NOT MODIFY UNLESS YOU KNOW WHAT YOU'RE DOING
# =============================================================================

pygame.init()
WIDTH = CELL_SIZE * GRID_WIDTH
HEIGHT = CELL_SIZE * GRID_HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Word Snake - ghicește cuvântul!")
clock = pygame.time.Clock()

# fonts (scales automatically with cell size)
font = pygame.font.SysFont(None, int(CELL_SIZE * 0.9))
ui_font = pygame.font.SysFont(None, int(CELL_SIZE * 1.5))

def spawn_letters(snake_body):
    """Spawns all the letters of the target word randomly on the board."""
    positions = set(snake_body)
    board_letters = []
    
    for char in TARGET_WORD:
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in positions:
                positions.add((x, y))
                board_letters.append({'char': char, 'pos': (x, y)})
                break
    return board_letters

def draw_grid():
    """Draws a faint grid to help players align the snake with letters."""
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))

def display_message(text, color):
    """Renders centered text on the screen."""
    msg_surface = ui_font.render(text, True, color)
    msg_rect = msg_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
    
    sub_surface = font.render("Apasă R pentru a restarta sau Q pentru a iesi", True, (200, 200, 200))
    sub_rect = sub_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
    
    screen.blit(msg_surface, msg_rect)
    screen.blit(sub_surface, sub_rect)

def main():
    # initial snake state
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    dx, dy = 1, 0  # moving right by default
    
    # target tracking
    letters_on_board = spawn_letters(snake)
    current_target_index = 0
    
    # same state
    state = "PLAYING" # can be PLAYING, WON, or LOST
    direction_changed = False # prevents rapid double-key press self-collisions

    while True:
        # --- 1. EVENT HANDLING ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if state == "PLAYING" and not direction_changed:
                    # 
                    if event.key in (pygame.K_UP, pygame.K_w) and dy == 0:
                        dx, dy = 0, -1
                        direction_changed = True
                    elif event.key in (pygame.K_DOWN, pygame.K_s) and dy == 0:
                        dx, dy = 0, 1
                        direction_changed = True
                    elif event.key in (pygame.K_LEFT, pygame.K_a) and dx == 0:
                        dx, dy = -1, 0
                        direction_changed = True
                    elif event.key in (pygame.K_RIGHT, pygame.K_d) and dx == 0:
                        dx, dy = 1, 0
                        direction_changed = True
                        
                elif state in ("WON", "LOST"):
                    if event.key == pygame.K_r:
                        main() # Restart the game
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

        if state == "PLAYING":
            # --- 2. GAME LOGIC ---
            head_x, head_y = snake[0]
            new_head = (head_x + dx, head_y + dy)
            
            # check wall collisions
            if not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT):
                state = "LOST"
                
            # check self collisions
            elif new_head in snake:
                state = "LOST"
                
            else:
                snake.insert(0, new_head)
                
                # check letter collisions
                hit_letter = None
                for letter in letters_on_board:
                    if letter['pos'] == new_head:
                        hit_letter = letter
                        break
                        
                if hit_letter:
                    expected_char = TARGET_WORD[current_target_index]
                    
                    if hit_letter['char'] == expected_char:
                        # correct letter! grow snake, move to next target
                        letters_on_board.remove(hit_letter)
                        current_target_index += 1
                        
                        # win condition met
                        if current_target_index == len(TARGET_WORD):
                            state = "WON"
                    else:
                        # wrong letter caught!
                        state = "LOST"
                else:
                    # didn't eat anything, remove the tail to maintain length
                    snake.pop()

            direction_changed = False # reset for the next frame

        # --- 3. DRAWING / RENDER ---
        screen.fill(BG_COLOR)
        draw_grid()

        # draw letters
        for letter in letters_on_board:
            char_surface = font.render(letter['char'], True, LETTER_COLOR)
            # Center the letter exactly inside the grid cell
            char_rect = char_surface.get_rect(
                center=(letter['pos'][0] * CELL_SIZE + CELL_SIZE // 2, 
                        letter['pos'][1] * CELL_SIZE + CELL_SIZE // 2)
            )
            screen.blit(char_surface, char_rect)

        # draw snake
        for i, segment in enumerate(snake):
            color = SNAKE_HEAD_COLOR if i == 0 else SNAKE_BODY_COLOR
            rect = pygame.Rect(segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            # draw slightly smaller than the cell size to create a segmented look
            pygame.draw.rect(screen, color, rect.inflate(-2, -2))
            
        # draw target ui (shows what to spell at the top)
        if state == "PLAYING":
            target_str = f"Cuvântul este: {TARGET_WORD[:current_target_index]}_"
            ui_surface = font.render(target_str, True, UI_TEXT_COLOR)
            screen.blit(ui_surface, (10, 10))

        # handle win/loss UI Overlays
        if state == "WON":
            display_message("ĂLA-I! BRAVO!", (50, 255, 50))
        elif state == "LOST":
            display_message("ASTA E.", (255, 50, 50))

        pygame.display.flip()
        clock.tick(GAME_SPEED)

if __name__ == "__main__":
    main()