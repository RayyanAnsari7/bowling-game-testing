"""
Bowling Game Implementation
A module for calculating bowling game scores.
"""

class BowlingGame:
    """Keeps track of a bowling game's rolls and calculates the final score."""

    def __init__(self):
        """Set up a new game with no rolls yet."""
        self.rolls = []
        self.current_frame = 1
        self.first_roll_this_frame = None

    def roll(self, pins):
        """Record one roll (ball) in the game.

        Checks that the number of pins is valid (0-10, and the two rolls
        in a frame don't add up to more than 10) before saving it.
        """
        if pins < 0:
            raise ValueError("Pins cannot be negative.")
        if pins > 10:
            raise ValueError("Pins cannot exceed 10.")

        if self.current_frame < 10:
            if self.first_roll_this_frame is None:
                if pins == 10:
                    self.current_frame += 1
                else:
                    self.first_roll_this_frame = pins
            else:
                if self.first_roll_this_frame + pins > 10:
                    raise ValueError("Frame total cannot exceed 10 pins.")
                self.first_roll_this_frame = None
                self.current_frame += 1

        self.rolls.append(pins)

    def score(self):
        """Add up the score for all 10 frames and return the total."""
        score = 0
        frame_index = 0

        for frame in range(10):
            if self._is_strike(frame_index):
                # Strike
                if frame_index + 2 >= len(self.rolls):
                    raise ValueError("Cannot score an incomplete game.")
                score += 10 + self._strike_bonus(frame_index)
                frame_index += 1
            elif self._is_spare(frame_index):
                # Spare
                if frame_index + 2 >= len(self.rolls):
                    raise ValueError("Cannot score an incomplete game.")
                score += 10 + self._spare_bonus(frame_index)
                frame_index += 2
            else:
                # Open frame
                if frame_index + 1 >= len(self.rolls):
                    raise ValueError("Cannot score an incomplete game.")
                score += self.rolls[frame_index] + self.rolls[frame_index + 1]
                frame_index += 2

        return score

    def _is_strike(self, frame_index):
        """Return True if the roll at this position knocked down all 10 pins."""
        return frame_index < len(self.rolls) and self.rolls[frame_index] == 10

    def _is_spare(self, frame_index):
        """Return True if the two rolls at this position add up to 10 pins."""
        return frame_index + 1 < len(self.rolls) and self.rolls[frame_index] + self.rolls[frame_index + 1] == 10

    def _strike_bonus(self, frame_index):
        """Return the bonus points earned after a strike (next two rolls)."""
        return self.rolls[frame_index + 1] + self.rolls[frame_index + 2]

    def _spare_bonus(self, frame_index):
        """Return the bonus points earned after a spare (next one roll)."""
        return self.rolls[frame_index + 2]