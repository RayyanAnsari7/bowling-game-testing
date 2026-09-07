"""
Bowling Game Implementation
A module for calculating bowling game scores.
"""

class BowlingGame:
    def __init__(self):
        # Initialize a new game with 10 frames
        # Each frame has up to 2 rolls (except the 10th frame which can have 3)
        self.rolls = []
        self.current_frame = 1
        self.first_roll_this_frame = None

    def roll(self, pins):
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
        
        return frame_index < len(self.rolls) and self.rolls[frame_index] == 10

    def _is_spare(self, frame_index):
        
        return frame_index + 1 < len(self.rolls) and self.rolls[frame_index] + self.rolls[frame_index + 1] == 10

    def _strike_bonus(self, frame_index):
       
        return self.rolls[frame_index + 1] + self.rolls[frame_index + 2]

    def _spare_bonus(self, frame_index):
       
        return self.rolls[frame_index + 2]