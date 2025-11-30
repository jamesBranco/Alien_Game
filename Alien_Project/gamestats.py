"""Game statistics for Alien Invasion (Lab 14)."""

class GameStats:
    """Track statistics for the game (score and active state)."""

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()
        # Start game in an inactive state; press Play to start.
        self.game_active = False

    def reset_stats(self):
        """Reset statistics that can change during the game."""
        self.score = 0