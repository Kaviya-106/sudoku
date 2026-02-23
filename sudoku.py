import pygame
import random


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
