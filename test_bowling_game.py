import pytest
from bowling_game import BowlingGame


# Fixture: reusable setup component
@pytest.fixture
def game():
    return BowlingGame()


def roll_many(game, rolls):
    """Helper to roll a list of pin values in sequence."""
    for pins in rolls:
        game.roll(pins)


def test_gutter_game(game):
    roll_many(game, [0] * 20)
    assert game.score() == 0


def test_all_ones(game):
    roll_many(game, [1] * 20)
    assert game.score() == 20


def test_one_spare(game):
    # Spare in frame 1, then a 3, rest zeros
    roll_many(game, [5, 5, 3] + [0] * 17)
    assert game.score() == 16


def test_one_strike(game):
    # Strike in frame 1, then 3 and 4, rest zeros
    roll_many(game, [10, 3, 4] + [0] * 16)
    assert game.score() == 24


def test_perfect_game(game):
    roll_many(game, [10] * 12)
    assert game.score() == 300


def test_all_spares(game):
    roll_many(game, [5] * 21)
    assert game.score() == 150


def test_regular_game_no_strikes_or_spares(game):
    rolls = [3, 4, 2, 5, 1, 6, 4, 2, 8, 1, 7, 1, 5, 3, 2, 3, 4, 3, 2, 6]
    roll_many(game, rolls)
    assert game.score() == 72


def test_open_tenth_frame(game):
    rolls = [0] * 18 + [4, 3]
    roll_many(game, rolls)
    assert game.score() == 7


def test_spare_in_tenth_frame(game):
    rolls = [0] * 18 + [5, 5, 7]
    roll_many(game, rolls)
    assert game.score() == 17


def test_strike_in_tenth_frame(game):
    rolls = [0] * 18 + [10, 5, 3]
    roll_many(game, rolls)
    assert game.score() == 18


# Parametrization: run the same assertion against several full games
@pytest.mark.parametrize("rolls, expected_score", [
    ([0] * 20, 0),
    ([1] * 20, 20),
    ([10] * 12, 300),
    ([5] * 21, 150),
])
def test_full_games(game, rolls, expected_score):
    roll_many(game, rolls)
    assert game.score() == expected_score


# --- Tests for bugs found during testing (invalid input handling) ---

def test_negative_pins_rejected(game):
    with pytest.raises(ValueError):
        game.roll(-1)


def test_pins_over_ten_rejected(game):
    with pytest.raises(ValueError):
        game.roll(11)


def test_frame_total_over_ten_rejected(game):
    game.roll(6)
    with pytest.raises(ValueError):
        game.roll(6)


def test_score_before_game_complete_raises_clear_error(game):
    game.roll(1)
    game.roll(2)
    with pytest.raises(ValueError):
        game.score()
