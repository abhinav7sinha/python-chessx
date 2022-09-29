from collections import defaultdict
from typing import Dict, List
import chess


# TODO: PeSTO's Evaluation Function
class PSQT:
    '''
    Class containing functionality for Piece Square Tables
    '''

    def __init__(self, fen: str):
        self.fen = fen
        self.piece_loc_map = self.build_piece_loc_map()
        self.psqt_map = self.build_psqt_map()
        self.piece_val_map = {
            'p': 100, 'n': 320, 'b': 330, 'r': 500, 'q': 900, 'k': 20000
        }

    def build_psqt_map(self) -> Dict[str, List[int]]:
        '''
        Returns a dictionary containing piece_symbols as keys and their
        respective piece square table array as values
        '''
        psqt_map = {}
        psqt_map['P'] = [
            0,  0,  0,  0,  0,  0,  0,  0,
            5, 10, 10, -20, -20, 10, 10,  5,
            5, -5, -10,  0,  0, -10, -5,  5,
            0,  0,  0, 20, 20,  0,  0,  0,
            5,  5, 10, 25, 25, 10,  5,  5,
            10, 10, 20, 30, 30, 20, 10, 10,
            50, 50, 50, 50, 50, 50, 50, 50,
            0,  0,  0,  0,  0,  0,  0,  0
        ]
        psqt_map['N'] = [
            -50, -40, -30, -30, -30, -30, -40, -50,
            -40, -20,  0,  5,  5,  0, -20, -40,
            -30,  5, 10, 15, 15, 10,  5, -30,
            -30,  0, 15, 20, 20, 15,  0, -30,
            -30,  5, 15, 20, 20, 15,  5, -30,
            -30,  0, 10, 15, 15, 10,  0, -30,
            -40, -20,  0,  0,  0,  0, -20, -40,
            -50, -40, -30, -30, -30, -30, -40, -50
        ]
        psqt_map['B'] = [
            -20, -10, -10, -10, -10, -10, -10, -20,
            -10,  5,  0,  0,  0,  0,  5, -10,
            -10, 10, 10, 10, 10, 10, 10, -10,
            -10,  0, 10, 10, 10, 10,  0, -10,
            -10,  5,  5, 10, 10,  5,  5, -10,
            -10,  0,  5, 10, 10,  5,  0, -10,
            -10,  0,  0,  0,  0,  0,  0, -10,
            -20, -10, -10, -10, -10, -10, -10, -20
        ]
        psqt_map['R'] = [
            0,  0,  0,  5,  5,  0,  0,  0,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            5, 10, 10, 10, 10, 10, 10,  5,
            0,  0,  0,  0,  0,  0,  0,  0
        ]
        psqt_map['Q'] = [
            -20, -10, -10, -5, -5, -10, -10, -20,
            -10,  0,  5,  0,  0,  0,  0, -10,
            -10,  5,  5,  5,  5,  5,  0, -10,
            0,  0,  5,  5,  5,  5,  0, -5,
            -5,  0,  5,  5,  5,  5,  0, -5,
            -10,  0,  5,  5,  5,  5,  0, -10,
            -10,  0,  0,  0,  0,  0,  0, -10,
            -20, -10, -10, -5, -5, -10, -10, -20
        ]
        psqt_map['K'] = [
            20, 30, 10,  0,  0, 10, 30, 20,
            20, 20,  0,  0,  0,  0, 20, 20,
            -10, -20, -20, -20, -20, -20, -20, -10,
            -20, -30, -30, -40, -40, -30, -30, -20,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
        ]
        psqt_map['p'] = psqt_map['P'][::-1]
        psqt_map['n'] = psqt_map['N'][::-1]
        psqt_map['b'] = psqt_map['B'][::-1]
        psqt_map['r'] = psqt_map['R'][::-1]
        psqt_map['q'] = psqt_map['Q'][::-1]
        psqt_map['k'] = psqt_map['K'][::-1]
        return psqt_map

    def build_piece_loc_map(self) -> Dict[str, List[int]]:
        '''
        Returns a dictionary containing piece_symbols as keys and their
        respective positions on the board as a list of integers using input FEN
        '''
        board = chess.Board(self.fen)
        piece_loc_map = defaultdict(list)
        for i in range(64):
            curr_piece = board.piece_at(i)
            if curr_piece:
                piece_loc_map[curr_piece.symbol()].append(i)
        return piece_loc_map

    def get_piece_eval(self, piece_symbol: str) -> int:
        '''
        Takes piece_symbol as input
        Returns board eval corresponding to just that piece
        '''
        white_eval = 0
        piece_type = piece_symbol.lower()
        for sq in self.piece_loc_map[piece_symbol.upper()]:
            white_eval += self.piece_val_map[piece_type]+self.psqt_map[piece_symbol.upper()][sq]
        black_eval = 0
        for sq in self.piece_loc_map[piece_symbol.lower()]:
            black_eval += self.piece_val_map[piece_type]+self.psqt_map[piece_symbol.lower()][sq]
        return white_eval-black_eval

    def get_explanations(self) -> List[str]:
        '''
        Returns list of explanations corresponding to each piece square table
        '''
        pieces = ['p', 'b', 'n', 'r', 'q', 'k']
        piece_name = {'p': 'Pawn(s)', 'n': 'Knight(s)', 'b': 'Bishop(s)', 'r': 'Rook(s)', 'q': 'Queen', 'k': 'King'}
        explanation_list = []
        for piece in pieces:
            if self.get_piece_eval(piece) > 0:
                explanation_list.append(f"White's {piece_name[piece]} is/are placed at better square(s) than Black")
            elif self.get_piece_eval(piece) < 0:
                explanation_list.append(f"Black's {piece_name[piece]} is/are placed at better square(s) than White")
        return explanation_list


if __name__ == '__main__':  # pragma: no cover
    fen_str = 'rn2kb1r/pp2qppp/2p2n2/4p1B1/2B1P3/1QN5/PPP2PPP/R3K2R b KQkq - 1 9'
    psqt = PSQT(fen_str)
    exp_list = psqt.get_explanations()
    print('PSQT Explanations:')
    for ex in exp_list:
        print(ex)
