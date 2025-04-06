import pygame
import random

pygame.init()


BLACK = (50, 50, 50)
WHITE = (150, 150, 150)
CYAN = (0, 150, 150)
YELLOW = (150, 150, 0)
PURPLE = (150, 0, 150)
RED = (150, 0, 0)
GREEN = (0, 150, 0)
BLUE = (0, 0, 150)
ORANGE = (255, 165, 0)
TEST = (255,255,255)

block_size = 30
grid_width = 10
grid_height = 20
width = block_size * grid_width
height = block_size * grid_height

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tetris")


grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]


shapes = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]]   # L
]

colors = [CYAN, YELLOW, PURPLE, GREEN, RED, BLUE, ORANGE]


piece_index = random.randint(0, len(shapes) - 1)
current_piece = shapes[piece_index]
piece_x = grid_width // 2 - len(current_piece[0]) // 2
piece_y = 0
piece_color = colors[piece_index]

clock = pygame.time.Clock()
running = True
fall_time = 0
fall_speed = 30  
score = 0

def check_collision(piece, x, y):
    for py, row in enumerate(piece):
        for px, cell in enumerate(row):
            if cell:
                new_x = x + px
                new_y = y + py
                if new_x < 0 or new_x >= grid_width or new_y >= grid_height or (new_y >= 0 and grid[new_y][new_x]):
                    return True
    return False

def rotate_piece(piece):
    
    return [list(row) for row in zip(*piece[::-1])]

def draw_grid():
    
    for y in range(grid_height):
        for x in range(grid_width):
            pygame.draw.rect(window, WHITE, (x * block_size, y * block_size, block_size, block_size), 1)

def draw_piece(piece, x, y, color):
    
    for py, row in enumerate(piece):
        for px, cell in enumerate(row):
            if cell:
                pygame.draw.rect(window, color, 
                                 ( (x + px) * block_size, (y + py) * block_size, block_size - 2, block_size - 2))

def clear_lines(grid):
    new_grid = [row for row in grid if any(cell == 0 for cell in row)]  
    cleared = grid_height - len(new_grid)
    new_grid = [[0 for _ in range(grid_width)] for _ in range(cleared)] + new_grid
    return new_grid, cleared
    


def game_over():
    running == False
    print("Ur score is: ", score)
    pygame.quit()



while running:
    fall_time += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a and not check_collision(current_piece, piece_x - 1, piece_y):
                piece_x -= 1
            if event.key == pygame.K_d and not check_collision(current_piece, piece_x + 1, piece_y):
                piece_x += 1
            if event.key == pygame.K_s and not check_collision(current_piece, piece_x, piece_y + 1):
                piece_y += 1
            if event.key == pygame.K_w:
                rotated = rotate_piece(current_piece)
                if not check_collision(rotated, piece_x, piece_y):
                    current_piece = rotated

    if fall_time >= fall_speed:
        if not check_collision(current_piece, piece_x, piece_y + 1):
            piece_y += 1
        else:
            for py, row in enumerate(current_piece):
                for px, cell in enumerate(row):
                    if cell:
                        grid[piece_y + py][piece_x + px] = piece_color  
            grid, cleared = clear_lines(grid)
            score += cleared * 10  
            piece_index = random.randint(0, len(shapes) - 1)
            current_piece = shapes[piece_index]
            piece_x = grid_width // 2 - len(current_piece[0]) // 2
            piece_y = 0
            piece_color = colors[piece_index]

        if check_collision(current_piece, piece_x, piece_y):
            if piece_y <= 0:
                game_over()
        fall_time = 0
            

    window.fill(BLACK)

    
    for y in range(grid_height):
        for x in range(grid_width):
            if grid[y][x]:
                pygame.draw.rect(window, grid[y][x], (x * block_size, y * block_size, block_size - 2, block_size - 2))

    


    draw_piece(current_piece, piece_x, piece_y, piece_color)

    
    draw_grid()




    pygame.display.update()
    clock.tick(30)

pygame.quit()
