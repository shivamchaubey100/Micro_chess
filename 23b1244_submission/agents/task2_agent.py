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

class Task2Agent(BaseAgent):
    def __init__(self, name="Task2Agent"):
        super().__init__(name)

    def reset(self):
        pass
 
    def _list_moves(self, board: Chess):
        pm, promo = board.legal_moves()
        return piece_matrix_to_legal_moves(pm, promo)

    def _piece_at(self, board, i, j):
        try:
            p = board.any_piece_at(i, j)
            if not p or p == -1:
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
                val = PIECE_VALUES.get(t, 0)
                s += val if c == 1 else -val
                if t == 0:  
                    if c == 1:
                        s += (4 - i) * 8
                    else:
                        s -= i * 8
        try:
            s += 5 * len(self._list_moves(board))
        except Exception:
            pass
        return s

    def _negamax(self, board, depth, alpha, beta, color):
        gr = board.game_result()
        if gr is not None:
            return gr * 20000 * color
        if depth == 0:
            return color * self._eval(board)

        moves = self._list_moves(board)
        if not moves:
            return color * self._eval(board)

        def key(m):
            (i,j),(dx,dy),promo = m
            ti, tj = i+dx, j+dy
            dest = self._piece_at(board, ti, tj)
            v = 0
            if dest:
                v += PIECE_VALUES.get(dest[0], 0)
            if promo != -1:
                v += 900
            return v
        moves = sorted(moves, key=key, reverse=True)

        if depth >= 3:
            moves = moves[:8]
        elif depth == 2:
            moves = moves[:10]

        best = -10**9
        for m in moves:
            child = self._make_child(board, m)
            val = -self._negamax(child, depth-1, -beta, -alpha, -color)
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
        alpha, beta = -10**9, 10**9
        best_move = random.choice(moves)
        best_val = -10**9

        def rkey(m):
            (i,j),(dx,dy),promo = m
            ti,tj = i+dx,j+dy
            dest = self._piece_at(board, ti, tj)
            v = 0
            if dest: v += PIECE_VALUES.get(dest[0],0)
            if promo != -1: v += 900
            return v
        moves = sorted(moves, key=rkey, reverse=True)[:12]

        for m in moves:
            child = self._make_child(board, m)
            val = -self._negamax(child, 3, -beta, -alpha, -color)  # total depth 4
            if val > best_val:
                best_val, best_move = val, m
            if val > alpha:
                alpha = val
        return best_move
