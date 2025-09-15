import pygame
import sys
import random
import math

from pathlib import Path
from player import player

# -- init --
pygame.init() # Initialize pygame
TILE = 32
SCREEN_W, SCREEN_H = 800, 600
window = pygame.display.set_mode((SCREEN_W, SCREEN_H)) # creates window surface you draw on
pygame.display.set_caption("2D Adventure Game") # Set title
clock = pygame.time.Clock() # limit frame rate (60 FPS) & measure delta time between frames

ASSETS = Path(__file__).parent / "assets" / "terrain"
SOLID = {"R", "T"}

# Player
player1 = player("Alex", "Male", "Human")
player_size = 31

SPEED = 250 # pixels per second

# Load tiles (convert_alpha for transparency + speed)
tiles = {
    "G": pygame.image.load(ASSETS / "grass.png").convert_alpha(),
    "W": pygame.image.load(ASSETS / "water.png").convert_alpha(),
    "R": pygame.image.load(ASSETS / "rock.png").convert_alpha(),
    "T": pygame.image.load(ASSETS / "trees.png").convert_alpha(),
}

# If any tile isn't exactly 32x32, force-resize:
for k, surf in tiles.items():
    if surf.get_size() != (TILE, TILE):
        tiles[k] = pygame.transform.smoothscale(surf, (TILE, TILE))

def get_tile(x, y):
    random.seed(hash((x, y))) # Deterministic seed
    r = random.random()
    
    if r < 0.7:
        return "G"
    elif r < 0.85:
        return "R"
    elif r < 0.95:
        return "T"
    else:
        return "W"


def draw_tilemap(surface, cam_x, cam_y):
    # How many tiles fit on screen (+2 for padding/offscreen scroll)
    tiles_x = SCREEN_W // TILE + 2
    tiles_y = SCREEN_H // TILE + 2

    # Which tile to start at (top left)
    # start_col = max(cam_x // TILE, 0)
    start_col = math.floor(cam_x / TILE)
    start_row = math.floor(cam_y / TILE)

    # start_row = max(cam_y // TILE, 0)

    for row in range(start_row, start_row + tiles_y):
        for col in range(start_col, start_col + tiles_x):
            ch = get_tile(col, row)
            tile = tiles.get(ch)
            if tile:
                screen_x = col * TILE - cam_x
                screen_y = row * TILE - cam_y
                surface.blit(tile, (screen_x, screen_y))

def is_blocked(tile_char):
    return tile_char in SOLID

# Game loop - loop that keeps the window open and the game running
running = True
while running:
    dt = clock.tick(60) / 1000.00 # cap loop at 60 iterations per second & returns milliseconds elasped since last tick
    # dt = delt time in seconds (ms / 1000.
    # if PC lags, dt gets bigger, so movement scales up to compensate. 'frame-rate independence'

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # input (continuous keys)
    keys = pygame.key.get_pressed() # array of booleans, one for each key on keyboard
    dx = dy = 0
    if keys[pygame.K_LEFT] or keys[pygame.K_a]: # Left
        dx -= SPEED * dt
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]: # Right
        dx += SPEED * dt
    if keys[pygame.K_UP] or keys[pygame.K_w]: # Up
        dy -= SPEED * dt
    if keys[pygame.K_DOWN] or keys[pygame.K_s]: # Down
        dy += SPEED * dt

    # update player
    player1.rect.x += int(dx)
    player1.rect.y += int(dy)

    # Camera - keep player at center of screen
    camera_x = player1.rect.centerx - SCREEN_W // 2
    camera_y = player1.rect.centery - SCREEN_H // 2

    # draw
    window.fill("black") # Set background color
    draw_tilemap(window, camera_x, camera_y)
    player_draw_rect = player1.image.get_rect()
    player_draw_rect.center = (SCREEN_W // 2, SCREEN_H // 2)
    window.blit(player1.image, player_draw_rect)
    pygame.display.flip()

pygame.quit()
sys.exit()