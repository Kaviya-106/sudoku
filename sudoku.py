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