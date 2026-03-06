import pygame
import random

REMOVE_COUNTS = {"Facile": 36, "Moyen": 46, "Difficile": 54}
DIFFICULTIES = ["Facile", "Moyen", "Difficile"]
SAVE_FILE = "sudoku_save.json"
FPS = 30


def is_valid(board, idx, val):
    row, col = divmod(idx, 9)
    br, bc = (row // 3) * 3, (col // 3) * 3
    for i in range(9):
        if board[row * 9 + i] == val:
            return False
        if board[i * 9 + col] == val:
            return False
        if board[(br + i // 3) * 9 + bc + i % 3] == val:
            return False
    return True


def shuffle(lst):
    lst = list(lst)
    random.shuffle(lst)
    return lst


def solve(board):
    try:
        empty = board.index(0)
    except ValueError:
        return True
    for n in shuffle(range(1, 10)):
        if is_valid(board, empty, n):
            board[empty] = n
            if solve(board):
                return True
            board[empty] = 0
    return False


def count_solutions(board, limit=2):
    try:
        empty = board.index(0)
    except ValueError:
        return 1
    count = 0
    for n in range(1, 10):
        if is_valid(board, empty, n):
            board[empty] = n
            count += count_solutions(board, limit)
            board[empty] = 0
            if count >= limit:
                return count
    return count


def generate_puzzle(difficulty):
    full = [0] * 81
    solve(full)
    solution = full[:]
    puzzle = full[:]
    to_remove = REMOVE_COUNTS[difficulty]
    removed = 0
    for idx in shuffle(range(81)):
        if removed >= to_remove:
            break
        backup = puzzle[idx]
        puzzle[idx] = 0
        if count_solutions(puzzle[:]) == 1:
            removed += 1
        else:
            puzzle[idx] = backup
    return puzzle, solution


class SudokuGame:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("SUDOKU")

        info = pygame.display.Info()
        self.screen_w = info.current_w
        self.screen_h = info.current_h
        self.fullscreen = False

        self.win_w = int(self.screen_w * 0.9)
        self.win_h = int(self.screen_h * 0.9)
        self.screen = pygame.display.set_mode(
            (self.win_w, self.win_h), pygame.RESIZABLE
        )
        self.clock = pygame.time.Clock()
        self.difficulty = "Moyen"
        self.diff_idx = 1
        self.btn_rects = []
        self.btn_callbacks = []

        self._rebuild_lay