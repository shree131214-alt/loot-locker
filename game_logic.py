"""Headless game rules for Loot Locker."""

import random
from collections import Counter
from collections.abc import Sequence


LOOT_SYMBOLS = ("◆", "●", "▲", "★", "♥", "☀", "☾", "✦")
CARDS_PER_PAIR = 2
BOARD_SIZE = len(LOOT_SYMBOLS) * CARDS_PER_PAIR


def create_deck(rng: random.Random | None = None) -> list[str]:
    """Return a shuffled deck containing two copies of every loot symbol."""
    deck = list(LOOT_SYMBOLS) * CARDS_PER_PAIR
    (rng or random.Random()).shuffle(deck)
    return deck


class GameState:
    """Track revealed and matched cards without depending on a GUI."""

    def __init__(self, deck: Sequence[str] | None = None) -> None:
        self.deck = list(deck) if deck is not None else create_deck()
        if len(self.deck) != BOARD_SIZE or Counter(self.deck) != Counter(
            {symbol: CARDS_PER_PAIR for symbol in LOOT_SYMBOLS}
        ):
            raise ValueError("A game deck must contain two of every loot symbol.")
        self.matched: set[int] = set()
        self.selected: list[int] = []
        self.turns = 0

    def reveal(self, index: int) -> bool:
        """Reveal a card if it can be selected; return whether it was revealed."""
        if not 0 <= index < BOARD_SIZE:
            return False
        if index in self.matched or index in self.selected or len(self.selected) == 2:
            return False
        self.selected.append(index)
        if len(self.selected) == 2:
            self.turns += 1
        return True

    def resolve_turn(self) -> bool:
        """Resolve the selected pair, returning True when it matches."""
        if len(self.selected) != 2:
            return False
        first, second = self.selected
        is_match = self.deck[first] == self.deck[second]
        if is_match:
            self.matched.update(self.selected)
        self.selected.clear()
        return is_match

    @property
    def is_won(self) -> bool:
        return len(self.matched) == BOARD_SIZE

