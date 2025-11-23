"""
Program: Alien Invasion (Lab 13)
Author: (James) Dyemydym Branco Vieira
Purpose: Based on Lab 12. Create a horizontal alien fleet aligned to the ship.
Aliens are removed when hit by bullets. If any alien hits the ship or
reaches the edge behind the rocket ship, the game is reset.
Date: 2025-11-23
"""

import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        # Create the game window.
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Alien Invasion - Lab 13")

        # Create the ship.
        self.ship = Ship(self)

        # Groups to hold bullets and aliens.
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        # Create initial fleet.
        self._create_fleet()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
            self._update_screen()
            self.clock.tick(60)  # Limit to 60 FPS

    # ========== Event handling ==========

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to key presses."""
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            pygame.quit()
            sys.exit()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    # ========== Bullets ==========

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old ones."""
        self.bullets.update()

        # Remove bullets that have moved off the right edge of the screen.
        for bullet in self.bullets.copy():
            if bullet.rect.left > self.settings.screen_width:
                self.bullets.remove(bullet)

        # Check for bullet–alien collisions and remove both.
        pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        # If all aliens are destroyed, create a new fleet.
        if not self.aliens:
            self._create_fleet()

    # ========== Aliens ==========

    def _update_aliens(self):
        """Update the positions of all aliens and handle collisions."""
        self.aliens.update()

        # 1) Check collision between ship and any alien.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._reset_game()
            return

        # 2) Check if any alien reached the left edge behind the ship.
        for alien in self.aliens.sprites():
            if alien.rect.left <= 0:
                self._reset_game()
                break

    def _reset_game(self):
        """Reset the game when ship is hit or aliens reach the left edge."""
        self.bullets.empty()
        self.aliens.empty()
        self.ship.center_ship()
        self._create_fleet()

    def _create_fleet(self):
        """Create a horizontal row of aliens on the right side."""
        self.aliens.empty()

        # Make a sample alien to get its size.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        # Space from ship to right edge for aliens.
        available_space_x = (
            self.settings.screen_width - self.ship.rect.width - 3 * alien_width
        )
        number_aliens = int(available_space_x // (2 * alien_width))

        # Place row roughly centered vertically.
        y_position = self.settings.screen_height // 2

        for alien_number in range(number_aliens):
            new_alien = Alien(self)
            # Position aliens from right to left in a row.
            new_alien.x = (
                self.settings.screen_width
                - alien_width
                - 2 * alien_width * alien_number
            )
            new_alien.rect.x = new_alien.x
            new_alien.rect.y = y_position
            self.aliens.add(new_alien)

    # ========== Drawing ==========

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        # Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)

        # Draw the ship, bullets, and aliens.
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Make the most recently drawn screen visible.
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
