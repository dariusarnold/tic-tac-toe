from itertools import *


def interleave(it1, count1, it2, count2):
    """
    Takes count1 elements from it1 and yields them, then count2 elements from it2 and yields them.
    Terminates on the shorter iterator.
    """
    try:
        while True:
            for _ in range(count1):
                yield next(it1)
            for _ in range(count2):
                yield next(it2)
    except StopIteration:
        pass


board_index = [7, 8, 9, 4, 5, 6, 1, 2, 3]


def format_board(content):
    return "".join(interleave(("{}" for _ in range(9)), 1, interleave(repeat("|"), 2, repeat("\n", 2), 1), 1)).format(*content)


def get_layout():
    return format_board(board_index)


def get_input(player_sign) -> int:
    while True:
        x = input(f"Player {player_sign}, enter an unoccupied position\n")
        if x.isdigit() and 0 < int(x) < 10:
            return int(x)
        else:
            print(f"Invalid input: {x}")


class Board:
    def __init__(self):
        self.EMPTY_CELL = " "
        self._board = [self.EMPTY_CELL] * 9

    def __str__(self):
        return format_board(self._board)

    def place(self, index, sign):
        self._board[index] = sign

    def is_occupied(self, index):
        return self._board[index] != self.EMPTY_CELL

    def _rows(self):
        for i in range(3):
            yield self._board[i*3:(i+1)*3]

    def _columns(self):
        for i in range(3):
            yield self._board[i::3]

    def _diagonals(self):
        yield self._board[::4]
        yield self._board[2:-1:2]

    def possible_lines(self):
        for i in chain(self._rows(), self._columns(), self._diagonals()):
            yield i

    def is_full(self):
        return self.EMPTY_CELL not in self._board


class Game:
    def __init__(self):
        self._board = Board()

    def _is_over(self):
        for line in self._board.possible_lines():
            s = set(line)
            if len(s) == 1 and self._board.EMPTY_CELL not in s:
                return True
        return False

    def play(self):
        active_player, next_player = ("X", "O")
        while not self._board.is_full():
            print(f"Player {active_player}'s turn")
            print(f"Layout\n{get_layout()}")
            print(f"Current board:\n{self._board}")
            while True:
                index = get_input(active_player) - 1
                index = board_index[index] - 1
                if not self._board.is_occupied(index):
                    break
            self._board.place(index, active_player)
            if self._is_over():
                print(f"Player {active_player} won")
                print(self._board)
                break

            active_player, next_player = next_player, active_player
            print()
        print("Draw")
        print(self._board)


def main():
    g = Game()
    g.play()


if __name__ == "__main__":
    main()