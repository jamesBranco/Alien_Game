import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to represent a single alien."""

    def __init__(self, ai_game):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the alien image and set rect.
        # Change filename here if your alien asset has a different name.
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Start each alien near the right side; we'll position it later.
        self.rect.x = self.settings.screen_width - self.rect.width
        self.rect.y = self.settings.screen_height // 2

        # Store the alien's exact horizontal position as a float.
        self.x = float(self.rect.x)

    def update(self):
        """Move the alien horizontally."""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x
