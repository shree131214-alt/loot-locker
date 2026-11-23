import unittest

from game_logic import BOARD_SIZE, LOOT_SYMBOLS, GameState, create_deck


class GameStateTests(unittest.TestCase):
    def test_new_deck_contains_two_of_each_symbol(self):
        deck = create_deck()

        self.assertEqual(len(deck), BOARD_SIZE)
        for symbol in LOOT_SYMBOLS:
            self.assertEqual(deck.count(symbol), 2)

    def test_revealing_two_cards_counts_one_turn_and_resolves_mismatch(self):
        game = GameState()

        self.assertTrue(game.reveal(0))
        self.assertTrue(game.reveal(1))
        self.assertEqual(game.turns, 1)
        self.assertFalse(game.resolve_turn())
        self.assertEqual(game.selected, [])
        self.assertEqual(game.matched, set())

    def test_matching_pair_stays_matched_and_cannot_be_revealed_again(self):
        deck = list(LOOT_SYMBOLS) * 2
        game = GameState(deck)

        self.assertTrue(game.reveal(0))
        self.assertTrue(game.reveal(8))
        self.assertTrue(game.resolve_turn())
        self.assertEqual(game.matched, {0, 8})
        self.assertFalse(game.reveal(0))

    def test_rejects_duplicate_and_out_of_range_selections(self):
        game = GameState()

        self.assertFalse(game.reveal(-1))
        self.assertFalse(game.reveal(BOARD_SIZE))
        self.assertTrue(game.reveal(0))
        self.assertFalse(game.reveal(0))
        self.assertEqual(game.turns, 0)

    def test_deck_must_have_exactly_two_of_each_symbol(self):
        with self.assertRaises(ValueError):
            GameState(["◆"] * BOARD_SIZE)

    def test_won_only_after_every_pair_is_resolved(self):
        game = GameState(list(LOOT_SYMBOLS) * 2)

        self.assertFalse(game.is_won)
        for first in range(len(LOOT_SYMBOLS)):
            self.assertTrue(game.reveal(first))
            self.assertTrue(game.reveal(first + len(LOOT_SYMBOLS)))
            self.assertTrue(game.resolve_turn())

        self.assertTrue(game.is_won)
        self.assertEqual(game.turns, len(LOOT_SYMBOLS))


if __name__ == "__main__":
    unittest.main()

