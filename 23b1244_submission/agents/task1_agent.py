from minichess.chess.fastchess import Chess
from .base_agent import BaseAgent
import random
from minichess.chess.fastchess_utils import piece_matrix_to_legal_moves

PIECE_VALUES = {
    0: 100,  # Pawn
    1: 320,  # Knight
    2: 330,  # Bishop
    3: 500,  # Rook
    4: 900,  # Queen
    5: 20000 # King
}

class Task1Agent(BaseAgent):
    def __init__(self, name="Task1Agent"):
        super().__init__(name)

    def reset(self): ...

    def _legal_moves(self, board: Chess):
        pm, promo = board.legal_moves()
        return piece_matrix_to_legal_moves(pm, promo)

    def _piece_at(self, board, i, j):
        p = board.any_piece_at(i, j)
        if not p or p == -1 or p[0] == -1:
            return None
        return p

    def _eval(self, board: Chess):
        score = 0
        for i in range(5):
            for j in range(4):
                p = self._piece_at(board, i, j)
                if not p:
                    continue
                t, c = p
                score += PIECE_VALUES[t] if c == 1 else -PIECE_VALUES[t]
        return score

    def move(self, board: Chess):
        try:
            if not board.has_legal_moves:
                return None
        except Exception:
            pass

        moves = self._legal_moves(board)
        if not moves:
            return None

        color = 1 if board.turn == 1 else -1
        best_val = -10**9
        best_move = random.choice(moves)

        def move_value(m):
            (i, j), (dx, dy), promo = m
            ti, tj = i + dx, j + dy
            p = self._piece_at(board, ti, tj)
            v = 0
            if p:
                v += PIECE_VALUES.get(p[0], 0)
            if promo != -1:
                v += 900
            return v

        moves.sort(key=move_value, reverse=True)

        moves = moves[:8]

        for m in moves:
            (i, j), (dx, dy), promo = m
            child = board.copy()
            child.make_move(i, j, dx, dy, promo)
            if child.game_result() is not None:
                val = child.game_result() * 20000 * color
            else:
                val = -10**9
                replies = self._legal_moves(child)
          
                replies.sort(key=move_value, reverse=True)
                replies = replies[:2]
                for r in replies:
                    (ii, jj), (ddx, ddy), pp = r
                    gc = child.copy()
                    gc.make_move(ii, jj, ddx, ddy, pp)
                    res = gc.game_result()
                    if res is not None:
                        leaf = res * 20000 * color
                    else:
                        leaf = -self._eval(gc) * color
                    if leaf > val:
                        val = leaf
                val = -val 

            if val > best_val:
                best_val = val
                best_move = m

        return best_move
