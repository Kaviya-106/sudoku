import pygame
import random
import sys
import time
import json
import os

BG = (15,  15,  15)
SURFACE = (26,  26,  26)
CELL_BG = (34,  34,  34)
CELL_GIVEN = (22,  22,  22)
BORDER_SOFT = (51,  51,  51)
BORDER_HARD = (136, 136, 136)
ACCENT = (232, 201, 122)
ACCENT2 = (122, 200, 232)
ERROR_COL = (232, 122, 122)
SUCCESS_COL = (122, 232, 160)
NOTE_COL = (110, 110, 110)
HIGHLIGHT = (30,  30,  40)
SELECTED_BG = (42,  42,  58)
SAME_NUM_BG = (30,  36,  32)
TEXT_MUTED = (100, 100, 100)
SAVE_COL = (160, 232, 160)

REMOVE_COUNTS = {"Facile": 36, "Moyen": 46, "Difficile": 54}
DIFFICULTIES = ["Facile", "Moyen", "Difficile"]
SAVE_FILE = "sudoku_save.json"
FPS = 30

# Les chiffres pour tous les types de pavés
NUM_KEYS = {
    pygame.K_1: 1, pygame.K_2: 2, pygame.K_3: 3,
    pygame.K_4: 4, pygame.K_5: 5, pygame.K_6: 6,
    pygame.K_7: 7, pygame.K_8: 8, pygame.K_9: 9,
    pygame.K_KP1: 1, pygame.K_KP2: 2, pygame.K_KP3: 3,
    pygame.K_KP4: 4, pygame.K_KP5: 5, pygame.K_KP6: 6,
    pygame.K_KP7: 7, pygame.K_KP8: 8, pygame.K_KP9: 9,
}

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

        self._rebuild_layout()
        self.new_game()
    
    def _rebuild_layout(self):
        W, H = self.screen.get_size()

        margin = int(min(W, H) * 0.04)
        ui_h = int(H * 0.24)
        title_h = int(H * 0.10)

        available = H - title_h - ui_h - margin * 2
        board_px = min(W - margin * 2, available)
        board_px = (board_px // 9) * 9

        self.BOARD_PX = board_px
        self.CELL = board_px // 9
        self.BOARD_X = (W - board_px) // 2
        self.BOARD_Y = title_h + margin
        self.UI_Y = self.BOARD_Y + board_px + margin
        self.W, self.H = W, H

        fs_title = max(16, int(H * 0.055))
        fs_cell = max(12, int(self.CELL * 0.52))
        fs_note = max(7,  int(self.CELL * 0.18))
        fs_ui = max(10, int(H * 0.022))
        fs_small = max(9,  int(H * 0.018))

        self.font_title = pygame.font.SysFont("Georgia", fs_title, bold=True)
        self.font_cell = pygame.font.SysFont("Courier New", fs_cell, bold=True)
        self.font_note = pygame.font.SysFont("Courier New", fs_note)
        self.font_ui = pygame.font.SysFont("Courier New", fs_ui)
        self.font_small = pygame.font.SysFont("Courier New", fs_small)
        
    def new_game(self):
        self.board, self.solution = generate_puzzle(self.difficulty)
        self.given = [v != 0 for v in self.board]
        self.notes = [set() for _ in range(81)]
        self.selected = -1
        self.note_mode = False
        self.hints_used = 0
        self.start_time = time.time()
        self.elapsed = 0
        self.running_timer = True
        self.status_msg = ""
        self.status_col = TEXT_MUTED
        self.won = False

# ── Timer ────────────────────────────────────────────────────────────────

    def get_time_str(self):
        t = int(self.elapsed)
        return f"{t // 60:02d}:{t % 60:02d}"

    # ── Saisie ───────────────────────────────────────────────────────────────

    def input_num(self, n):
        if self.selected == -1:
            self.set_status("Selectionnez d'abord une cellule !", TEXT_MUTED)
            return
        if self.given[self.selected]:
            self.set_status("Cette case est fixe !", TEXT_MUTED)
            return
        if self.note_mode and self.board[self.selected] == 0:
            if n in self.notes[self.selected]:
                self.notes[self.selected].discard(n)
            else:
                self.notes[self.selected].add(n)
        else:
            self.board[self.selected] = n
            self.notes[self.selected].clear()
        self.check_win()

    def erase_cell(self):
        if self.selected == -1 or self.given[self.selected]:
            return
        self.board[self.selected] = 0
        self.notes[self.selected].clear()
        
    def hint(self):
        candidates = [
            i for i in range(81)
            if not self.given[i] and self.board[i] != self.solution[i]
        ]
        if not candidates:
            return
        idx = random.choice(candidates)
        self.board[idx] = self.solution[idx]
        self.notes[idx].clear()
        self.selected = idx
        self.hints_used += 1
        self.set_status(f"Indice utilise ({self.hints_used} total)", ERROR_COL)
        self.check_win()

    def check_board(self):
        errors = sum(
            1 for i in range(81)
            if self.board[i] != 0 and self.board[i] != self.solution[i]
        )
        if errors == 0 and 0 in self.board:
            self.set_status("Aucune erreur pour l'instant !", ACCENT)
        elif errors > 0:
            self.set_status(f"{errors} erreur(s) trouvee(s)", ERROR_COL)
        else:
            self.check_win()

    def check_win(self):
        if 0 not in self.board and all(
            self.board[i] == self.solution[i] for i in range(81)
        ):
            self.running_timer = False
            self.won = True
            hint_str = f"avec {self.hints_used} indice(s)" if self.hints_used else""
            self.set_status(
                f"Bravo ! Resolu en {self.get_time_str()}{hint_str} !",
                SUCCESS_COL
            )

    def set_status(self, msg, col):
        self.status_msg = msg
        self.status_col = col
    
    def save_game(self):
        data = {
            "board":      self.board,
            "solution":   self.solution,
            "given":      self.given,
            "notes":      [list(s) for s in self.notes],
            "difficulty": self.difficulty,
            "diff_idx":   self.diff_idx,
            "elapsed":    int(self.elapsed),
            "hints_used": self.hints_used,
            "saved_at":   time.strftime("%d/%m/%Y %H:%M"),
        }
        try:
            with open(SAVE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            self.set_status(f"Sauvegarde ! ({data['saved_at']})", SAVE_COL)
        except Exception as e:
            self.set_status(f"Erreur sauvegarde : {e}", ERROR_COL)

    def load_game(self):
        if not os.path.exists(SAVE_FILE):
            self.set_status("Aucune sauvegarde trouvee.", TEXT_MUTED)
            return
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.board = data["board"]
            self.solution = data["solution"]
            self.given = data["given"]
            self.notes = [set(s) for s in data["notes"]]
            self.difficulty = data["difficulty"]
            self.diff_idx = data["diff_idx"]
            self.elapsed = data["elapsed"]
            self.hints_used = data["hints_used"]
            self.selected = -1
            self.note_mode = False
            self.won = False
            self.running_timer = True
            self.start_time = time.time() - self.elapsed
            saved_at = data.get("saved_at", "?")
            self.set_status(f"Partie du {saved_at} chargee !", SAVE_COL)
        except Exception as e:
            self.set_status(f"Erreur chargement : {e}", ERROR_COL)

    def save_exists(self):
        return os.path.exists(SAVE_FILE)
    
    def draw(self):
        self.screen.fill(BG)
        self._draw_title()
        self._draw_board()
        self._draw_ui()
        pygame.display.flip()

    def _draw_title(self):
        W, H = self.W, self.H
        title = self.font_title.render("SUDOKU", True, ACCENT)
        self.screen.blit(title, (W//2 - title.get_width() // 2, int(H*0.012)))
        sub = self.font_small.render("PUZZLE CLASSIQUE", True, TEXT_MUTED)
        self.screen.blit(sub, (W // 2 - sub.get_width() // 2, int(H * 0.065)))

    def _draw_board(self):
        BX, BY, C = self.BOARD_X, self.BOARD_Y, self.CELL

        for i in range(81):
            row, col = divmod(i, 9)
            x = BX + col * C
            y = BY + row * C

            if i == self.selected:
                color = SELECTED_BG
            elif self.selected != -1:
                sr, sc = divmod(self.selected, 9)
                sb = (sr // 3) * 3 + sc // 3
                cb = (row // 3) * 3 + col // 3
                if row == sr or col == sc or sb == cb:
                    color = HIGHLIGHT
                elif self.board[self.selected] != 0 and self.board[i] == self.board[self.selected]:
                    color = SAME_NUM_BG
                else:
                    color = CELL_GIVEN if self.given[i] else CELL_BG
            else:
                color = CELL_GIVEN if self.given[i] else CELL_BG

            pygame.draw.rect(self.screen, color, (x, y, C, C))

            val = self.board[i]
            if val != 0:
                is_err = not self.given[i] and val != self.solution[i]
                txt_col = ERROR_COL if is_err else (ACCENT if not self.given[i] else ACCENT2)
                surf = self.font_cell.render(str(val), True, txt_col)
                self.screen.blit(surf, (
                    x + C // 2 - surf.get_width() // 2,
                    y + C // 2 - surf.get_height() // 2
                ))
            elif self.notes[i]:
                nc_s = C // 3
                for n in range(1, 10):
                    if n in self.notes[i]:
                        nr, nc = divmod(n - 1, 3)
                        ns = self.font_note.render(str(n), True, NOTE_COL)
                        self.screen.blit(ns, (
                            x + nc * nc_s + max(2, nc_s // 5),
                            y + nr * nc_s + max(1, nc_s // 6)
                        ))

        BP = self.BOARD_PX
        for i in range(10):
            thick = max(2, C // 18) if i % 3 == 0 else 1
            col_v = BORDER_HARD if i % 3 == 0 else BORDER_SOFT
            pygame.draw.line(self.screen, col_v, (BX + i * C, BY), (BX + i * C, BY + BP), thick)
            pygame.draw.line(self.screen, col_v, (BX, BY + i * C), (BX + BP, BY + i * C), thick)

    def _draw_ui(self):
        W, UI_Y, H = self.W, self.UI_Y, self.H

        ts = self.font_ui.render(self.get_time_str(), True, TEXT_MUTED)
        self.screen.blit(ts, (W // 2 - ts.get_width() // 2, UI_Y - int(H * 0.032)))

        buttons = [
            (f"< {self.difficulty} >", self._btn_diff),
            ("NOUVELLE PARTIE",         self.new_game),
            (f"NOTES {'ON' if self.note_mode else 'OFF'}", self._toggle_notes),
            ("INDICE  [H]",             self.hint),
            ("EFFACER",                 self.erase_cell),
            ("VERIFIER",                self.check_board),
            ("SAUVEGARDER  [S]",        self.save_game),
            ("CHARGER PARTIE",          self.load_game),
            ("PLEIN ECRAN  [F11]",      self.toggle_fullscreen),
        ]

        per_row = 3
        total_w = W - int(W * 0.06)
        btn_w = (total_w - (per_row - 1) * int(W * 0.015)) // per_row
        btn_h = max(24, int(H * 0.038))
        start_x = int(W * 0.03)
        gap_x = int(W * 0.015)
        gap_y = int(H * 0.010)

        self.btn_rects = []
        self.btn_callbacks = []

        for i, (label, cb) in enumerate(buttons):
            row_i, col_i = divmod(i, per_row)
            bx = start_x + col_i * (btn_w + gap_x)
            by = UI_Y + row_i * (btn_h + gap_y)
            rect = pygame.Rect(bx, by, btn_w, btn_h)
            self.btn_rects.append(rect)
            self.btn_callbacks.append(cb)

            is_note = (i == 2)
            is_save = (i == 6)
            is_load = (i == 7)

            if is_note and self.note_mode:
                border, txt = ACCENT2, ACCENT2
            elif is_save:
                border, txt = SAVE_COL, SAVE_COL
            elif is_load:
                has_save = self.save_exists()
                border = SAVE_COL if has_save else BORDER_SOFT
                txt = SAVE_COL if has_save else TEXT_MUTED
            else:
                border, txt = BORDER_SOFT, ACCENT

            pygame.draw.rect(self.screen, SURFACE, rect)
            pygame.draw.rect(self.screen, border, rect, 1)

            lbl = self.font_small.render(label, True, txt)
            if lbl.get_width() > btn_w - 8:
                f2 = pygame.font.SysFont("Courier New", max(7, self.font_small.size(" ")[1] - 2))
                lbl = f2.render(label, True, txt)

            self.screen.blit(lbl, (
                rect.centerx - lbl.get_width() // 2,
                rect.centery - lbl.get_height() // 2
            ))

        if self.status_msg:
            sm = self.font_small.render(self.status_msg, True, self.status_col)
            rows = (len(buttons) + per_row - 1) // per_row
            sy = UI_Y + rows * (btn_h + gap_y) + int(H * 0.008)
            self.screen.blit(sm, (W // 2 - sm.get_width() // 2, sy))

    def _btn_diff(self):
        self.cycle_difficulty()

    def _toggle_notes(self):
        self.note_mode = not self.note_mode
