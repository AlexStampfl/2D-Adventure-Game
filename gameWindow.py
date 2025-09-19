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
    "T": [
        pygame.image.load(TERRAIN / "trees" / "my_pixel_tree.png").convert_alpha(),
        pygame.image.load(TERRAIN / "trees" / "tree_variant_1.png").convert_alpha()
    ]

    # "default": pygame.image.load(TERRAIN / "grass" / "grass_variant_1.png").convert_alpha()
}
for k, surf, in tiles.items():
    if isinstance(surf, list):
        for i in range(len(surf)):
            if surf[i].get_size() != (TILE, TILE):
                surf[i] = pygame.transform.scale(surf[i], (TILE, TILE)).convert_alpha()
    else:
        if surf.get_size() != (TILE, TILE):
            tiles[k] = pygame.transform.scale(surf, (TILE, TILE)).convert_alpha()
            # print(tiles["R"].get_flags() & pygame.SRCALPHA)

TILE_SIZE = 48

LAKE_DISTANCE = 25 # min distance between lakes
LAKE_RADIUS = 3 # controls size of lakes
LAKE_CHANCE = 0.3 # % of map tiles considered for lake centers
MAP_WIDTH = 100
MAP_HEIGHT = 100

lake_centers = []

def is_far_enough(x, y):
    for lx, ly in lake_centers:
        if math.hypot(lx - x, ly - y) < LAKE_DISTANCE: # take time to understand this later
            return False
    return True

def generate_lake_center(map_width, map_height):
    for x in range(0, map_width, 4):
        for y in range(0, map_height, 4):
            random.seed(hash((x, y)))
            if random.random() < LAKE_CHANCE:
                if is_far_enough(x, y):
                    lake_centers.append((x, y))
    print(f"Lake center added at ({x}, {y})")

generate_lake_center(MAP_WIDTH, MAP_HEIGHT)



# Take time to understand this more later


def is_water(x, y):
    for lx, ly in lake_centers:
        if math.hypot(x - lx, y - ly) <= LAKE_RADIUS:
            return True
    return False

def get_tile(x, y):
    if is_water(x, y):
        return "W"
    
    random.seed(hash((x, y))) # Deterministic seed
    r = random.random()
    
    if r < 0.8:
        return "G"
    elif r < 0.85:
        return "R"
    elif r < 0.95:
        return "T"
    else:
        return "G"

def choose_tile(key):
    tile_entry = tiles.get(key)
    if isinstance(tile_entry, list):
        return random.choice(tile_entry)
    return tile_entry

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

            tile = choose_tile(ch)

            if ch in {"T", "R"}:
                # Always draw a base grass tile first - BIG ISSUE resolved. This took forever to figure out
                bg = random.choice(tiles["G"])
                surface.blit(bg, (screen_x, screen_y))
            tile = choose_tile(ch)
            surface.blit(tile, (screen_x, screen_y)) # Critical to terrain visibility


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


    pygame.display.flip() # Critical to game being visible

pygame.quit()
sys.exit()