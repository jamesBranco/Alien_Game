import pygame


class Ship:
    """A class to manage the ship."""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and rotate it to face right.
        original_image = pygame.image.load('images/ship.bmp')
        # In the book, the ship faces up; rotate 270° to make it face right.
        self.image = pygame.transform.rotate(original_image, 270)
        self.rect = self.image.get_rect()

        # Start the ship on the left border, vertically centered.
        self.rect.midleft = self.screen_rect.midleft

        # Store a float for the ship's vertical position.
        self.y = float(self.rect.y)

        # Movement flags
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Update the ship's position based on movement flags."""
        # Move up
        if self.moving_up and self.rect.top > 0:
            self.y -= 1.5
        # Move down
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += 1.5

        # Update rect object from self.y
        self.rect.y = self.y

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
