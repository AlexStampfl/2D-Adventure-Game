import pygame
import sys
import random
import math
import os

from pathlib import Path
from player import Player

# -- init --
pygame.init() # Initialize pygame
TILE = 48

SCREEN_W, SCREEN_H = 800, 600
window = pygame.display.set_mode((SCREEN_W, SCREEN_H)) # creates window surface you draw on
pygame.display.set_caption("2D Adventure Game") # Set title
clock = pygame.time.Clock() # limit frame rate (60 FPS) & measure delta time between frames

ASSETS = Path(__file__).parent / "assets"
TERRAIN = ASSETS / "terrain"
PLAYER = ASSETS / "player"

SOLID = {"R", "T"}

SPEED = 200 # pixels per second


def load_animations(path):
    directions = ["down", "left", "right", "up"]
    animations = {}

    for direction in directions:
        frames = []
        for i in range(3):
            filename = f"{direction}_{i}.png"
            full_path = os.path.join(path, filename)
            image = pygame.image.load(full_path).convert_alpha()
            frames.append(image)
        animations[direction] = frames

    return animations


animations = load_animations("assets/player")
player1 = Player(300, 300, animations)


# Load terrain tiles
tiles = {
    "G":[ # G for grass
        pygame.image.load(TERRAIN / "grass" / "grass_variant_1.png").convert_alpha(),
        pygame.image.load(TERRAIN / "grass" / "grass_variant_2.png").convert_alpha(),
        pygame.image.load(TERRAIN / "grass"/ "grass_variant_3.png").convert_alpha(),
        pygame.image.load(TERRAIN / "grass" / "grass_variant_4.png").convert_alpha(),
    ],
    "W": pygame.image.load(TERRAIN / "water.png").convert_alpha(),
    "R": pygame.image.load(TERRAIN / "rock.png").convert_alpha(),
    "T": pygame.image.load(TERRAIN / "my_pixel_tree.png").convert_alpha(),

    "default": pygame.image.load(TERRAIN / "grass" / "grass_variant_1.png").convert_alpha()
}

# If any tile isn't exactly 32x32, force-resize:
for k, surf in tiles.items():
    # if k != "T" and surf.get_size() != (TILE, TILE):
    if k == "G" or k == "T":
        continue
    if surf.get_size() != (TILE, TILE):
        tiles[k] = pygame.transform.smoothscale(surf, (TILE, TILE))

TILE_SIZE = 48

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

    tiles_x = SCREEN_W // TILE + 2
    tiles_y = SCREEN_H // TILE + 2

    start_col = math.floor(cam_x / TILE)
    start_row = math.floor(cam_y / TILE)

    # tile-drawing loop
    for row in range(start_row, start_row + tiles_y):
        for col in range(start_col, start_col + tiles_x):
            ch = get_tile(col, row)
            screen_x = col * TILE - cam_x
            screen_y = row * TILE - cam_y

            if ch == "G":
                tile = random.choice(tiles["G"])
            else:
                tile = tiles.get(ch)
                if tile is None:
                    tile = tiles["default"]
            surface.blit(tile, (screen_x, screen_y))

def is_blocked(tile_char):
    return tile_char in SOLID

# Game loop - loop that keeps the window open and the game running
running = True
while running:
    keys = pygame.key.get_pressed()
    dt = clock.tick(60) / 1000.00 # cap loop at 60 iterations per second & returns milliseconds elasped since last tick
    player1.update(keys, dt)
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

    # Camera - keep player at center of screen
    camera_x = player1.rect.centerx - SCREEN_W // 2
    camera_y = player1.rect.centery - SCREEN_H // 2

    # draw
    window.fill((106, 190, 48)) # Set background color
    draw_tilemap(window, camera_x, camera_y)

    player_draw_rect = player1.image.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2))
    # window.blit(player1.image, player1.rect)
    window.blit(player1.image, player_draw_rect) # keeps the player at the center of the screen


    pygame.display.flip()

pygame.quit()
sys.exit()