# settings.py

class Settings:
    """A class to store all configuration settings."""

    def __init__(self):
        """Initialize the game's settings."""

        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Bullet settings (for the projectile)
        self.bullet_speed = 5.0
        self.bullet_width = 15
        self.bullet_height = 3
        self.bullet_color = (60, 60, 60)

        # Alien settings
        self.alien_speed = 1.0       # how fast aliens move horizontally
        self.fleet_direction = -1    # -1 = move left (toward ship)
