"""
Program: Alien Invasion (Lab 14)
Author: Dyemydym (James) Branco Vieira
Purpose: Extend Lab 13 by adding a Play button, HUD (score), and hiding
         the cursor while the game is active.
Date: 2025-11-30
"""

import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from gamestats import GameStats
from scoreboard import Scoreboard
from button import Button


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
        pygame.display.set_caption("Alien Invasion - Lab 14")

        # Game statistics and HUD
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # Ship and sprite groups
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        # Create initial fleet (shown behind Play button)
        self._create_fleet()

        # Play button
        self.play_button = Button(self, "Play")

    # ---------------- MAIN LOOP ----------------
    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(60)

    # -------------- EVENT HANDLING --------------
    def _check_events(self):
        """Respond to keypresses, mouse events, and quitting."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        """Respond to key presses."""
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE and self.stats.game_active:
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

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        clicked = self.play_button.rect.collidepoint(mouse_pos)
        if clicked and not self.stats.game_active:
            # Reset the game statistics.
            self.stats.reset_stats()
            self.stats.game_active = True

            # Clear existing aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Reset HUD.
            self.sb.prep_score()

            # Hide the mouse cursor while playing.
            pygame.mouse.set_visible(False)

    # ---------------- BULLETS ----------------
    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        bullet = Bullet(self)
        self.bullets.add(bullet)

    def _update_bullets(self):
        """Update position of bullets, and handle collisions."""
        self.bullets.update()

        # Remove bullets beyond right edge
        for bullet in self.bullets.copy():
            if bullet.rect.left > self.settings.screen_width:
                self.bullets.remove(bullet)

        # Check for bullet–alien collisions
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )

        if collisions:
            # Each alien hit gives points.
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()

        # If all aliens are destroyed, create a new fleet.
        if not self.aliens:
            self._create_fleet()

    # ---------------- ALIENS ----------------
    def _update_aliens(self):
        """Move aliens and check for collisions with ship or left edge."""
        self.aliens.update()

        # Alien hits ship
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._end_round()

        # Alien reaches left edge
        for alien in self.aliens.sprites():
            if alien.rect.left <= 0:
                self._end_round()
                break

    def _end_round(self):
        """Handle losing a round (ship hit or aliens reach left edge)."""
        self.stats.game_active = False

        # Show cursor again for clicking Play.
        pygame.mouse.set_visible(True)

        # Clear sprites and re-center ship.
        self.bullets.empty()
        self.aliens.empty()
        self.ship.center_ship()
        self._create_fleet()

    def _create_fleet(self):
        """Create a horizontal line of aliens on the right side."""
        self.aliens.empty()

        # Make one alien to find its width/height.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        # Space available between ship and right edge.
        available_space_x = (
            self.settings.screen_width - self.ship.rect.width - 3 * alien_width
        )
        number_aliens = int(available_space_x // (2 * alien_width))

        # Keep aliens roughly centered vertically.
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

    # ---------------- SCREEN DRAW ----------------
    def _update_screen(self):
        """Draw everything to the screen."""
        self.screen.fill(self.settings.bg_color)

        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Draw the score.
        self.sb.show_score()

        # Draw the Play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()
