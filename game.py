from board import Board


class Game:
    def __init__(self):
        self.board = Board()
        self.best_score = 0
        self.history = []

    def display(self):
        print("\n" + "+------+------+------+------+")

        for row in self.board.grid:
            print(
                "|"
                + "|".join(
                    f"{x:^6}" if x else f"{' ':^6}"
                    for x in row
                )
                + "|"
            )

            print("+------+------+------+------+")

        print("Score:", self.board.score, " Best:", self.best_score)

    def move(self, key):
        moves = {
            "a": self.board.move_left,
            "d": self.board.move_right,
            "w": self.board.move_up,
            "s": self.board.move_down
        }

        if key not in moves:
            return False

        old_grid = [row[:] for row in self.board.grid]
        old_score = self.board.score

        changed = moves[key]()

        if changed:
            self.history = [(old_grid, old_score)]
            self.board.add_random_tile()
            self.best_score = max(
                self.best_score,
                self.board.score
            )

        return changed

    def undo(self):
        if not self.history:
            print("Nothing to undo.")
            return False

        grid, score = self.history.pop()

        self.board.grid = [row[:] for row in grid]
        self.board.score = score

        print("Move undone.")
        return True

    def run(self):
        print("2048 — W/A/S/D to move, U to undo, Q to quit.")

        while True:
            self.display()

            if self.board.has_won():
                print("You reached 2048!")
                return

            if not self.board.can_move():
                print("No legal moves remain.")
                return

            key = input("> ").strip().lower()

            if key == "q":
                return

            if key == "u":
                self.undo()
                continue

            if key not in "wasd":
                print("Use W/A/S/D.")
                continue

            self.move(key)