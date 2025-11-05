from minichess.chess.fastchess import Chess
from .base_agent import BaseAgent
import random
from minichess.chess.fastchess_utils import piece_matrix_to_legal_moves

PIECE_VALUES = {
    0: 100, 1: 320, 2: 330, 3: 500, 4: 900, 5: 20000
}

class Task4Agent(BaseAgent):
    def __init__(self, name="Task4Agent"):
        super().__init__(name)

    def reset(self): ...

    def _list_moves(self, board: Chess):
        pm, promo = board.legal_moves()
        return piece_matrix_to_legal_moves(pm, promo)

    def _piece_at(self, board, i, j):
        try:
            p = board.any_piece_at(i, j)
            if p is None or p == -1 or p[0] == -1:
                return None
            return p
        except Exception:
            return None

    def _make_child(self, board, move):
        (i, j), (dx, dy), promo = move
        b = board.copy()
        b.make_move(i, j, dx, dy, promo)
        return b

    def _eval(self, board):
        s = 0
        for i in range(5):
            for j in range(4):
                pc = self._piece_at(board, i, j)
                if not pc:
                    continue
                t, c = pc
                v = PIECE_VALUES.get(t, 0)
                s += v if c == 1 else -v

                if t == 0:
                    s += (4 - i) * 8 if c == 1 else -i * 8

                if t != 0:
                    center_bonus = 6 - (abs(2 - i) + abs(1.5 - j))
                    s += (center_bonus * 4 if c == 1 else -center_bonus * 4)

        try:
            s += 5 * len(self._list_moves(board))
        except Exception:
            pass
        return s

    def _is_capture(self, board, move):
        (i, j), (dx, dy), _ = move
        ti, tj = i + dx, j + dy
        dest = self._piece_at(board, ti, tj)
        return dest is not None

    def _immediate_danger(self, child, our_color):
        try:
            replies = self._list_moves(child)
        except Exception:
            return 0
        caps = [r for r in replies if self._is_capture(child, r)]
        if not caps:
            return 0
        worst = 0
        for r in caps[:6]:
            cc = self._make_child(child, r)
            d = self._eval(cc) - self._eval(child)
            if our_color == 1:
                worst = min(worst, d)
            else:
                worst = max(worst, d)
        return abs(worst) if abs(worst) > 150 else 0

    def _negamax(self, board, depth, alpha, beta, color):
        gr = board.game_result()
        if gr is not None:
            return gr * 20000 * color
        if depth == 0:
            return color * self._eval(board)

        moves = self._list_moves(board)
        if not moves:
            return color * self._eval(board)

        def k(m):
            (i, j), (dx, dy), promo = m
            ti, tj = i + dx, j + dy
            dest = self._piece_at(board, ti, tj)
            v = 0
            if dest:
                v += PIECE_VALUES.get(dest[0], 0)
            if promo != -1:
                v += 900
            return v

        moves = sorted(moves, key=k, reverse=True)

        if depth >= 3:
            moves = moves[:6]
        elif depth == 2:
            moves = moves[:8]

        best = -10**9
        for m in moves:
            child = self._make_child(board, m)
            next_depth = depth - 1
         
            if self._is_capture(board, m) or m[2] != -1:
                next_depth = depth
            val = -self._negamax(child, next_depth, -beta, -alpha, -color)
            if val > best:
                best = val
            if best > alpha:
                alpha = best
            if alpha >= beta:
                break
        return best

    def move(self, board: Chess):
        try:
            if not board.has_legal_moves:
                return None
        except Exception:
            pass

        moves = self._list_moves(board)
        if not moves:
            return None

        color = 1 if board.turn == 1 else -1

        def rk(m):
            (i, j), (dx, dy), promo = m
            ti, tj = i + dx, j + dy
            dest = self._piece_at(board, ti, tj)
            v = 0
            if dest:
                v += PIECE_VALUES.get(dest[0], 0)
            if promo != -1:
                v += 900
            return v

        moves = sorted(moves, key=rk, reverse=True)[:10]

        best_move, best_val = random.choice(moves), -10**9
        alpha, beta = -10**9, 10**9

        for m in moves:
            child = self._make_child(board, m)
            penalty = self._immediate_danger(child, color)
            val = -self._negamax(child, 2, -beta, -alpha, -color) - penalty
            if val > best_val:
                best_val, best_move = val, m
            if val > alpha:
                alpha = val

        return best_move
