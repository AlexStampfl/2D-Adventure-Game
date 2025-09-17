import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, animations):
        super().__init__()
        self.animations = animations
        self.direction = "down"
        self.frame = 0
        self.image = self.animations[self.direction][self.frame]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.animation_timer = 0

    def update(self, keys_pressed, dt):
        speed = 150  # pixels per second
        dx = dy = 0

        if keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]:
            self.direction = "up"
            dy -= speed * dt
        if keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
            self.direction = "down"
            dy += speed * dt
        if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
            self.direction = "left"
            dx -= speed * dt
        if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
            self.direction = "right"
            dx += speed * dt

        self.rect.x += int(dx)
        self.rect.y += int(dy)

        # Animation
        if dx != 0 or dy != 0:
            self.animation_timer += dt
            if self.animation_timer > 0.15:
                self.frame = (self.frame + 1) % 3
                self.animation_timer = 0
        else:
            self.frame = 0  # idle

        self.image = self.animations[self.direction][self.frame]