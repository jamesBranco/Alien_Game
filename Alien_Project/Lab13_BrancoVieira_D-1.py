"""
Program: Alien Invasion (Lab 13)
Author: (James) Dyemydym Branco Vieira
Purpose: Added alien fleet, bullet–alien collisions,
and game resets when aliens hit the ship or reach the left edge.
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

        # Create game window
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Alien Invasion - Lab 13")

        # Create ship
        self.ship = Ship(self)

        # Create sprite groups
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        # Create initial alien fleet
        self._create_fleet()

    # -------------------------------------------------
    # MAIN GAME LOOP
    # -------------------------------------------------
    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
            self._update_screen()
            self.clock.tick(60)

    # -------------------------------------------------
    # EVENT HANDLING
    # -------------------------------------------------
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

    # -------------------------------------------------
    # BULLETS
    # -------------------------------------------------
    def _fire_bullet(self):
        """Fire a bullet from the ship."""
        bullet = Bullet(self)
        self.bullets.add(bullet)

    def _update_bullets(self):
        """Move bullets and remove old ones."""
        self.bullets.update()

        # Remove bullets beyond right edge
        for bullet in self.bullets.copy():
            if bullet.rect.left > self.settings.screen_width:
                self.bullets.remove(bullet)

        # Remove bullets & aliens when they collide
        pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )

        # If no aliens left, create a new fleet
        if not self.aliens:
            self._create_fleet()

    # -------------------------------------------------
    # ALIENS
    # -------------------------------------------------
    def _update_aliens(self):
        """Move aliens and check for collisions."""
        self.aliens.update()

        # 1. Alien hits ship
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._reset_game()
            return

        # 2. Alien reaches left edge (behind ship)
        for alien in self.aliens.sprites():
            if alien.rect.left <= 0:
                self._reset_game()
                return

    def _reset_game(self):
        """Reset game state."""
        self.bullets.empty()
        self.aliens.empty()
        self.ship.center_ship()
        self._create_fleet()

    # -------------------------------------------------
    # FLEET CREATION
    # -------------------------------------------------
    def _create_fleet(self):
        """Create a horizontal line of aliens on the right side."""
        self.aliens.empty()

        # Make one alien to get width/height
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        # Space between ship and right edge
        available_space_x = (
            self.settings.screen_width - self.ship.rect.width - 3 * alien_width
        )

        number_aliens = int(available_space_x // (2 * alien_width))

        # Keep aliens vertically aligned with ship (center)
        y_position = self.settings.screen_height // 2

        for alien_number in range(number_aliens):
            new_alien = Alien(self)
            new_alien.x = (
                self.settings.screen_width
                - alien_width
                - (2 * alien_width * alien_number)
            )
            new_alien.rect.x = new_alien.x
            new_alien.rect.y = y_position
            self.aliens.add(new_alien)

    # -------------------------------------------------
    # SCREEN UPDATES
    # -------------------------------------------------
    def _update_screen(self):
        """Draw everything to the screen."""
        self.screen.fill(self.settings.bg_color)

        # Draw elements
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Refresh screen
        pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
