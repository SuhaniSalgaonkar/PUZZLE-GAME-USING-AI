import pygame
import random
import time
from puzzle import Puzzle
from ai_solver import a_star_solver
import tkinter as tk
from tkinter import messagebox

pygame.init()

# Global game state
size = 3
tile_size = 170
screen_width = (tile_size * size + 20) * 2
screen_height = tile_size * size + 200
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Sliding Puzzle with AI")

font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
BLUE = (139,69,19)

# Load & prepare background
def load_background():
    global background
    background = pygame.image.load("background.jpg").convert()
    background = pygame.transform.scale(background, (screen_width, screen_height))
load_background()

# Create semi-transparent overlay
overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)


puzzle1 = None
puzzle2 = None

start_time1 = None
elapsed_time1 = 0
elapsed_time2 = 0
move_count1 = 0
ai_move_count = 0
game_started1 = False
ai_done = False
player_done = False
ai_solving = False

tile_images = []

def load_and_slice_image():
    global tile_images, tile_size, size
    full_image = pygame.image.load("puzzle_image.jpg").convert()
    full_image = pygame.transform.scale(full_image, (tile_size * size, tile_size * size))

    tile_images = []
    for row in range(size):
        row_images = []
        for col in range(size):
            rect = pygame.Rect(col * tile_size, row * tile_size, tile_size, tile_size)
            image_piece = full_image.subsurface(rect).copy()
            row_images.append(image_piece)
        tile_images.append(row_images)
        
def load_and_slice_imagee():
    global tile_images, tile_size, size
    full_image = pygame.image.load("puzzle_imagee.jpg").convert()
    full_image = pygame.transform.scale(full_image, (tile_size * size, tile_size * size))

    tile_images = []
    for row in range(size):
        row_images = []
        for col in range(size):
            rect = pygame.Rect(col * tile_size, row * tile_size, tile_size, tile_size)
            image_piece = full_image.subsurface(rect).copy()
            row_images.append(image_piece)
        tile_images.append(row_images)
def load_and_slice_imageee():
    global tile_images, tile_size, size
    full_image = pygame.image.load("puzzle_imageee.jpg").convert()
    full_image = pygame.transform.scale(full_image, (tile_size * size, tile_size * size))

    tile_images = []
    for row in range(size):
        row_images = []
        for col in range(size):
            rect = pygame.Rect(col * tile_size, row * tile_size, tile_size, tile_size)
            image_piece = full_image.subsurface(rect).copy()
            row_images.append(image_piece)
        tile_images.append(row_images)        

def draw_board():
    screen.blit(background, (0, 0))
    screen.blit(overlay, (0, 0))

    def draw_tile(i, val, offset_x=15):
        x = (i % size) * tile_size + offset_x
        y = (i // size) * tile_size + 50
        if val == 0:
          
            
          
            return  # Skip image and text for blank tile
        # Draw white background for other tiles (optional)
        pygame.draw.rect(screen, WHITE, (x, y, tile_size, tile_size), border_radius=1)
        # Draw tile image
        row, col = divmod(val - 1, size)
        screen.blit(tile_images[row][col], (x, y))
        # Draw black border on top
        pygame.draw.rect(screen, BLACK, (x, y, tile_size, tile_size), 1, border_radius=1)
        # Draw tile number with shadow
        display_number = str(val)
        number_text = font.render(display_number, True, BLACK)
        shadow_text = font.render(display_number, True, WHITE)
        screen.blit(shadow_text, (x + 11, y + 11))
        screen.blit(number_text, (x + 10, y + 10))

    for i, val in enumerate(puzzle1.board):
        draw_tile(i, val)

    offset_x = tile_size * size + 20
    for i, val in enumerate(puzzle2.board):
        draw_tile(i, val, offset_x)

    pygame.draw.rect(screen, BLUE, (17, tile_size * size + 70, 100, 30))
    pygame.draw.rect(screen, BLUE, (127, tile_size * size + 70, 100, 30))
    screen.blit(font.render("Shuffle", True, BLACK), (25, tile_size * size + 75))
    screen.blit(font.render("Reset", True, BLACK), (145, tile_size * size + 75))

    screen.blit(font.render("Player", True, BLACK), (10, 10))
    screen.blit(font.render("AI", True, BLACK), (screen_width // 2 + 10, 10))

    screen.blit(font.render(f"Moves: {move_count1}", True, BLACK), (17, tile_size * size + 120))
    if game_started1 and not player_done:
        now = time.time()
        screen.blit(font.render(f"Time: {now - start_time1:.1f}s", True, BLACK), (150, tile_size * size + 120))
    elif player_done:
        screen.blit(font.render(f"Time: {elapsed_time1:.1f}s", True, BLACK), (150, tile_size * size + 120))

    if ai_done:
        screen.blit(font.render(f"AI Moves: {ai_move_count}", True, BLACK), (screen_width // 2 + 10, tile_size * size + 120))
        screen.blit(font.render(f"AI Time: {elapsed_time2:.1f}s", True, BLACK), (screen_width // 2 + 200, tile_size * size + 120))

def get_clicked_tile(pos):
    x, y = pos
    if y >= tile_size * size + 70:
        if 10 <= x <= 110:
            return "shuffle"
        elif 120 <= x <= 220:
            return "reset"
        return None
    col = x // tile_size
    row = (y - 50) // tile_size
    return row * size + col

def move_tile(index):
    global move_count1
    blank = puzzle1.board.index(0)
    r1, c1 = divmod(blank, size)
    r2, c2 = divmod(index, size)
    if abs(r1 - r2) + abs(c1 - c2) == 1:
        puzzle1.board[blank], puzzle1.board[index] = puzzle1.board[index], puzzle1.board[blank]
        move_count1 += 1

def shuffle_puzzles():
    global puzzle1, puzzle2, move_count1, ai_move_count, start_time1
    global game_started1, ai_solving, ai_done, player_done

    goal_state = list(range(1, size * size)) + [0]
    puzzle1 = Puzzle(size, goal_state)
    puzzle2 = Puzzle(size, goal_state)

    for _ in range(50):
        move = random.choice(puzzle1.get_possible_moves())
        puzzle1.move(move)
        puzzle2.move(move)

    move_count1 = 0
    ai_move_count = 0
    start_time1 = None
    game_started1 = False
    ai_solving = False
    ai_done = False
    player_done = False

def reset_game():
    global puzzle1, puzzle2, move_count1, ai_move_count, start_time1
    global game_started1, ai_solving, ai_done, player_done

    goal_state = list(range(1, size * size)) + [0]
    puzzle1 = Puzzle(size, goal_state)
    puzzle2 = Puzzle(size, goal_state)

    move_count1 = 0
    ai_move_count = 0
    start_time1 = None
    game_started1 = False
    ai_solving = False
    ai_done = False
    player_done = False

def show_popup(player_time, player_moves, ai_time, ai_moves):
    root = tk.Tk()
    root.withdraw()
    message = (
        f"🏁 Puzzle Completed!\n\n"
        f"👤 Player - Time: {player_time:.1f}s | Moves: {player_moves}\n"
        f"🤖 AI     - Time: {ai_time:.1f}s | Moves: {ai_moves}"
    )
    messagebox.showinfo("Result", message)
    root.destroy()

def start_ai():
    global ai_done, ai_solving, elapsed_time2, ai_move_count
    ai_solving = True
    start_time2 = time.time()
    moves = a_star_solver(puzzle2.board)
    for move in moves:
        puzzle2.move(move)
        ai_move_count += 1
        draw_board()
        pygame.display.flip()
        time.sleep(1)
    elapsed_time2 = time.time() - start_time2
    ai_done = True

def game_loop():
    global start_time1, elapsed_time1, game_started1, player_done
    running = True
    while running:
        draw_board()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = get_clicked_tile(pos)
                if clicked == "shuffle":
                    shuffle_puzzles()
                elif clicked == "reset":
                    reset_game()
                elif isinstance(clicked, int) and clicked < size * size:
                    if not player_done:
                        if not game_started1:
                            game_started1 = True
                            start_time1 = time.time()
                        move_tile(clicked)
                        if puzzle1.is_solved():
                            player_done = True
                            elapsed_time1 = time.time() - start_time1
                            pygame.time.set_timer(pygame.USEREVENT, 1000)
            elif event.type == pygame.USEREVENT:
                if player_done and not ai_solving and not ai_done:
                    pygame.time.set_timer(pygame.USEREVENT, 0)
                    start_ai()
                    if ai_done:
                        show_popup(elapsed_time1, move_count1, elapsed_time2, ai_move_count)

        clock.tick(60)

def difficulty_menu():
    global size, tile_size, screen, screen_width, screen_height
    global puzzle1, puzzle2, overlay, background

    tile_size = 170
    size = 3
    screen_width = (tile_size * size + 20) * 2
    screen_height = tile_size * size + 200
    screen = pygame.display.set_mode((screen_width, screen_height))

    background = pygame.image.load("background.jpg").convert()
    background = pygame.transform.scale(background, (screen_width, screen_height))

    overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    

    while True:
        screen.blit(background, (0, 0))
        screen.blit(overlay, (0, 0))

        title_text = font.render("Select Difficulty", True, BLACK)
        screen.blit(title_text, ((screen_width - title_text.get_width()) // 2, 220))

        button_width = 250
        button_height = 50
        spacing = 20
        total_height = 3 * button_height + 2 * spacing
        start_y = (screen_height - total_height) // 2 + 50

        easy_button = pygame.Rect((screen_width - button_width) // 2, start_y, button_width, button_height)
        med_button = pygame.Rect((screen_width - button_width) // 2, start_y + button_height + spacing, button_width, button_height)
        hard_button = pygame.Rect((screen_width - button_width) // 2, start_y + 2 * (button_height + spacing), button_width, button_height)

        pygame.draw.rect(screen, BLUE, easy_button, border_radius=12)
        pygame.draw.rect(screen, BLUE, med_button, border_radius=12)
        pygame.draw.rect(screen, BLUE, hard_button, border_radius=12)

        screen.blit(font.render("Easy (3x3)", True, BLACK), (easy_button.x + 70, easy_button.y + 10))
        screen.blit(font.render("Medium (4x4)", True, BLACK), (med_button.x + 60, med_button.y + 10))
        screen.blit(font.render("Hard (5x5)", True, BLACK), (hard_button.x + 70, hard_button.y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button.collidepoint(event.pos):
                    size = 3
                    
                elif med_button.collidepoint(event.pos):
                    size = 4
                    
                elif hard_button.collidepoint(event.pos):
                    size = 5
                else:
                    continue

                tile_size = 600 // size
                screen_width = (tile_size * size + 20) * 2
                screen_height = tile_size * size + 200
                screen = pygame.display.set_mode((screen_width, screen_height))

                background = pygame.image.load("background.jpg").convert()
                background = pygame.transform.scale(background, (screen_width, screen_height))
                overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
                

                if easy_button.collidepoint(event.pos):
                    size = 3
                    load_and_slice_imageee()
                elif med_button.collidepoint(event.pos):
                    size = 4
                    load_and_slice_imagee()
                elif hard_button.collidepoint(event.pos):
                    size = 5
                    load_and_slice_image()


                goal = list(range(1, size * size)) + [0]
                puzzle1 = Puzzle(size, goal)
                puzzle2 = Puzzle(size, goal)

                game_loop()
                return

def start_menu():
    global screen, screen_width, screen_height, overlay, background

    # Set menu screen size and title
    screen_width = (tile_size * size + 20) * 2
    screen_height = tile_size * size + 200
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Sliding Puzzle with AI - Start Menu")

    background = pygame.image.load("background.jpg").convert()
    background = pygame.transform.scale(background, (screen_width, screen_height))

    overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    

    button_width, button_height = 250, 60
    button_x = (screen_width - button_width) // 2
    button_y = (screen_height - button_height) // 2

    play_button = pygame.Rect(button_x, button_y, button_width, button_height)

    running = True
    while running:
        screen.blit(background, (0, 0))
        screen.blit(overlay, (0, 0))

        title_text = font.render("Welcome to Sliding Puzzle with AI", True, BLACK)
        screen.blit(title_text, ((screen_width - title_text.get_width()) // 2, button_y - 100))

        pygame.draw.rect(screen, BLUE, play_button, border_radius=15)
        screen.blit(font.render("Play Now", True, BLACK), (play_button.x + 75, play_button.y + 15))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    difficulty_menu()
                    running = False

    pygame.quit()

if __name__ == "__main__":
    start_menu()

