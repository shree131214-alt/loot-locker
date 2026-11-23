# Build Loot Locker step by step

Loot Locker is a desktop memory game: reveal two cards, remember their symbols, and find all eight pairs. The interface uses Python's built-in Tkinter; no extra packages are needed.

## 1. Set up the project

**Goal:** Keep the game rules, window, and tests in separate files.

Create `game_logic.py`, `app.py`, and `tests/test_game_logic.py`. This separation lets Python test the game rules without creating a Tkinter window.

**Check:** From the project folder, run `python --version` and confirm Python 3.10 or later is available.

## 2. Prepare the treasure deck

**Goal:** Make a deck with two copies of each symbol and shuffle it.

In `game_logic.py`, look at `LOOT_SYMBOLS`, `BOARD_SIZE`, and `create_deck`. The standard-library `random.Random` shuffles the symbols; every new game gets a different card order.

**Check:** Run `python -m unittest -v`. The deck test checks that there are 16 cards and exactly two of every symbol.

## 3. Track selections and matches

**Goal:** Implement the rules independently of the desktop interface.

In `game_logic.py`, `GameState.reveal` accepts a selectable card and counts a turn when the second card is revealed. `resolve_turn` compares the two symbols, saves matching card positions, and clears the current selection. `is_won` becomes true when all cards are matched.

**Check:** Run `python -m unittest -v` again. The tests cover invalid and duplicate clicks, mismatches, matches, turn counts, and winning.

## 4. Create the native window and card grid

**Goal:** Show the game as an interactive desktop app.

In `app.py`, `main` creates a `tk.Tk` root window, constructs `LootLockerApp`, and starts Tkinter's `mainloop` event loop. `_build_window` arranges headings, score labels, and 16 `tk.Button` cards with `Frame` containers and `pack`/`grid` layout.

Each card button's `command` is a callback: a function Tkinter calls when the player clicks that card. The `lambda` captures that card's index so each button reports the right position.

**Check:** Run `python app.py`. A native window should open with a 4-by-4 grid of face-down cards.

## 5. Connect clicks to game rules

**Goal:** Reveal cards, check pairs, and update the window.

In `app.py`, `_on_card_clicked` calls `GameState.reveal` and refreshes the button labels and colors. When two cards are selected, it schedules `_resolve_turn` with `root.after(700, ...)`. `after` lets Tkinter handle the short delay through its event loop, so the player can see both cards before a mismatch is hidden.

The `StringVar` values for the turn count, pair count, and status message connect game progress to their labels. `_start_new_game` replaces the game state and refreshes the same window.

**Check:** Click two cards. Matching symbols stay green; mismatches turn face-down after a short pause. Find all eight pairs and confirm the win message.

## 6. Run tests and play again

**Goal:** Verify the rules and practice a fresh round.

The tests in `tests/test_game_logic.py` import only `game_logic.py`, not `app.py`, so they do not need a display server or open a GUI window. `.github/workflows/tests.yml` runs the same standard-library tests with Python 3.12 on pushes and pull requests.

**Check:** Run `python -m unittest -v`, then launch `python app.py` and select **Shuffle & play again**.

