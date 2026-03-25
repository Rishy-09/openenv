
from typing import List
from openenv.core.env_server import Action, Observation, State


class WordGameAction(Action):
    """Player guesses a single letter."""
    guess: str


class WordGameObservation(Observation):
    """What the player sees after each guess.

    Note: done and reward are inherited from Observation.
    """
    masked_word: str            # e.g. "p_th_n"
    guessed_letters: List[str]  # All letters tried
    attempts_remaining: int
    message: str                # Feedback text


class WordGameState(State):
    """Episode metadata.

    Note: episode_id and step_count are inherited from State.
    """
    target_word: str = ""
    max_attempts: int = 10
