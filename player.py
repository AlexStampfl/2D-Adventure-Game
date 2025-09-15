import pygame

# Player class
class player(pygame.sprite.Sprite):
    def __init__(self, name, gender, race):
        super().__init__() # Always call this first when using pygame.sprite.Sprite
        self.name = name
        self.gender = gender
        self.race = race

        self.size = 31
        self.image = pygame.Surface((self.size, self.size)) # Make a square
        self.image.fill((50, 150, 255)) # blue
        self.rect = self.image.get_rect()
        self.rect.center = (0, 0) # world position

player1 = player("Alex", "Male", "Human")