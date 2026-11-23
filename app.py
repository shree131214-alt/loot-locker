"""Tkinter desktop interface for Loot Locker."""

import tkinter as tk
from tkinter import ttk

from game_logic import BOARD_SIZE, GameState


BACKGROUND = "#111827"
PANEL = "#1f2937"
CARD_BACK = "#334155"
CARD_FACE = "#f8fafc"
ACCENT = "#fbbf24"
MUTED = "#94a3b8"


class LootLockerApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Loot Locker")
        self.root.configure(bg=BACKGROUND)
        self.root.resizable(False, False)
        self.root.minsize(470, 640)

        self.game = GameState()
        self.locked = False
        self.pending_resolve: str | None = None
        self.cards: list[tk.Button] = []
        self.turn_text = tk.StringVar()
        self.pair_text = tk.StringVar()
        self.message_text = tk.StringVar()

        self._build_window()
        self._refresh_board()
        self._update_score()

    def _build_window(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Restart.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=(12, 8),
            background=ACCENT,
            foreground="#1f2937",
        )
        style.map("Restart.TButton", background=[("active", "#fcd34d")])

        outer = tk.Frame(self.root, bg=BACKGROUND, padx=24, pady=22)
        outer.pack(fill="both", expand=True)

        tk.Label(
            outer,
            text="LOOT LOCKER",
            bg=BACKGROUND,
            fg=ACCENT,
            font=("Segoe UI", 22, "bold"),
        ).pack(anchor="w")
        tk.Label(
            outer,
            text="Find every matching pair in the treasure chest.",
            bg=BACKGROUND,
            fg=MUTED,
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(3, 18))

        score_panel = tk.Frame(outer, bg=PANEL, padx=16, pady=12)
        score_panel.pack(fill="x", pady=(0, 16))
        tk.Label(
            score_panel, textvariable=self.turn_text, bg=PANEL, fg="#f8fafc",
            font=("Segoe UI", 11, "bold"),
        ).pack(side="left")
        tk.Label(
            score_panel, textvariable=self.pair_text, bg=PANEL, fg="#f8fafc",
            font=("Segoe UI", 11, "bold"),
        ).pack(side="right")

        board = tk.Frame(outer, bg=BACKGROUND)
        board.pack()
        for index in range(BOARD_SIZE):
            card = tk.Button(
                board,
                text="?",
                command=lambda card_index=index: self._on_card_clicked(card_index),
                width=5,
                height=2,
                bg=CARD_BACK,
                fg="#e2e8f0",
                activebackground="#475569",
                activeforeground="#ffffff",
                disabledforeground="#ffffff",
                relief="flat",
                bd=0,
                font=("Segoe UI Symbol", 18, "bold"),
                cursor="hand2",
                takefocus=True,
            )
            card.grid(row=index // 4, column=index % 4, padx=5, pady=5, sticky="nsew")
            self.cards.append(card)

        self.message_label = tk.Label(
            outer,
            textvariable=self.message_text,
            bg=BACKGROUND,
            fg=MUTED,
            font=("Segoe UI", 10),
            height=2,
        )
        self.message_label.pack(fill="x", pady=(12, 4))

        footer = tk.Frame(outer, bg=BACKGROUND)
        footer.pack(fill="x")
        ttk.Button(
            footer, text="Shuffle & play again", style="Restart.TButton",
            command=self._start_new_game,
        ).pack(side="left")
        tk.Label(
            footer,
            text="Click two cards to reveal their loot.",
            bg=BACKGROUND,
            fg=MUTED,
            font=("Segoe UI", 9),
        ).pack(side="right", padx=(8, 0))

    def _on_card_clicked(self, index: int) -> None:
        if self.locked or not self.game.reveal(index):
            return
        self._refresh_board()
        if len(self.game.selected) == 2:
            self.locked = True
            self.message_text.set("Checking your loot…")
            self.pending_resolve = self.root.after(700, self._resolve_turn)

    def _resolve_turn(self) -> None:
        self.pending_resolve = None
        matched = self.game.resolve_turn()
        self.locked = False
        if matched:
            self.message_text.set("A match! The loot is yours.")
        else:
            self.message_text.set("No match this time. Keep looking!")
        self._refresh_board()
        self._update_score()
        if self.game.is_won:
            self.message_text.set(f"All loot found in {self.game.turns} turns. Nicely played!")

    def _start_new_game(self) -> None:
        if self.pending_resolve is not None:
            self.root.after_cancel(self.pending_resolve)
            self.pending_resolve = None
        self.game = GameState()
        self.locked = False
        self.message_text.set("Good luck, treasure hunter!")
        self._refresh_board()
        self._update_score()

    def _refresh_board(self) -> None:
        for index, card in enumerate(self.cards):
            if index in self.game.matched:
                card.configure(
                    text=self.game.deck[index], bg="#166534", fg="#f0fdf4",
                    state="disabled", cursor="arrow",
                )
            elif index in self.game.selected:
                card.configure(
                    text=self.game.deck[index], bg=CARD_FACE, fg="#111827",
                    state="disabled" if self.locked else "normal",
                    cursor="arrow" if self.locked else "hand2",
                )
            else:
                card.configure(
                    text="?", bg=CARD_BACK, fg="#e2e8f0",
                    state="disabled" if self.locked else "normal",
                    cursor="arrow" if self.locked else "hand2",
                )

    def _update_score(self) -> None:
        self.turn_text.set(f"Turns  {self.game.turns}")
        pairs_found = len(self.game.matched) // 2
        self.pair_text.set(f"Pairs  {pairs_found}/8")


def main() -> None:
    root = tk.Tk()
    LootLockerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

