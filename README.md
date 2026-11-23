# Loot Locker

**Gaming project for 2026-11-07**

Loot Locker is a small, beginner-friendly memory game. Match eight pairs of treasure symbols in a polished native desktop window built with Python's Tkinter. It needs no external packages, and gameplay happens entirely in the window.

## Build it step by step

Follow the ordered **[BUILD_GUIDE.md](BUILD_GUIDE.md)** tutorial to build the actual game from its rules to its Tkinter interface.

## Launch the desktop game

Requires Python 3.10 or later. Open a terminal in this folder and run:

```bash
python app.py
```

Click any two cards to reveal them. Find all eight pairs, then use **Shuffle & play again** for another round.

## Run the tests

The rules are separate from Tkinter, so tests run without opening a desktop window:

```bash
python -m unittest -v
```

## Project files

- `app.py` — the Tkinter window, card buttons, layout, and click/timer callbacks.
- `game_logic.py` — shuffled deck and testable match rules.
- `tests/` — standard-library unit tests for the game rules.
- `.github/workflows/tests.yml` — automated tests on Python 3.12.

