"""
Program: Alien Invasion (Lab 13)
Author: Dyemydym (James) Branco Vieira
Purpose: Build on Lab 12. Add alien fleet, bullet–alien collisions,
and reset the game if an alien hits the ship or reaches the left edge.
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

    # ---------------------------------------------------------
    # MAIN GAME LOOP
    # ---------------------------------------------------------
    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self.ship.update()
            self._up_
