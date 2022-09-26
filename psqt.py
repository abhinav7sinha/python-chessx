import os
os.system('cls' if os.name == 'nt' else 'clear')

from collections import defaultdict
import chess

# TODO: PeSTO's Evaluation Function
class PSQT:
    '''
    Based on Tomasz Michniewski's Simple Evaluation Function
    We've ignored the end game table for the king
    currently on evaluating middlegame positions
    '''
    def __init__(self, fen):
        self.fen=fen
        self.pieces=['Pawn']
        self.piece_square_dict=self.get_piece_square_dict(fen)
        self.piece_square_table={}
        self.piece_val={
            'p': 100, 'P': 100, 'n': 320, 'N': 320, 'b': 330, 'B': 330,
            'r': 500, 'R': 500, 'q': 900, 'Q': 900, 'k': 20000, 'K': 20000
        }

        self.p_val=100
        self.n_val=320
        self.b_val=330
        self.r_val=500
        self.q_val=900
        self.k_val=20000

        self.piece_square_table['P'] = [
            0,  0,  0,  0,  0,  0,  0,  0,
            5, 10, 10,-20,-20, 10, 10,  5,
            5, -5,-10,  0,  0,-10, -5,  5,
            0,  0,  0, 20, 20,  0,  0,  0,
            5,  5, 10, 25, 25, 10,  5,  5,
            10, 10, 20, 30, 30, 20, 10, 10,
            50, 50, 50, 50, 50, 50, 50, 50,
            0,  0,  0,  0,  0,  0,  0,  0
        ]
        self.piece_square_table['N'] = [
            -50,-40,-30,-30,-30,-30,-40,-50,
            -40,-20,  0,  5,  5,  0,-20,-40,
            -30,  5, 10, 15, 15, 10,  5,-30,
            -30,  0, 15, 20, 20, 15,  0,-30,
            -30,  5, 15, 20, 20, 15,  5,-30,
            -30,  0, 10, 15, 15, 10,  0,-30,
            -40,-20,  0,  0,  0,  0,-20,-40,
            -50,-40,-30,-30,-30,-30,-40,-50
            ]
        self.piece_square_table['B'] = [
            -20,-10,-10,-10,-10,-10,-10,-20,
            -10,  5,  0,  0,  0,  0,  5,-10,
            -10, 10, 10, 10, 10, 10, 10,-10,
            -10,  0, 10, 10, 10, 10,  0,-10,
            -10,  5,  5, 10, 10,  5,  5,-10,
            -10,  0,  5, 10, 10,  5,  0,-10,
            -10,  0,  0,  0,  0,  0,  0,-10,
            -20,-10,-10,-10,-10,-10,-10,-20
        ]
        self.piece_square_table['R'] = [
            0,  0,  0,  5,  5,  0,  0,  0,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            5, 10, 10, 10, 10, 10, 10,  5,
            0,  0,  0,  0,  0,  0,  0,  0
        ]
        self.piece_square_table['Q'] = [
            -20,-10,-10, -5, -5,-10,-10,-20,
            -10,  0,  5,  0,  0,  0,  0,-10,
            -10,  5,  5,  5,  5,  5,  0,-10,
            0,  0,  5,  5,  5,  5,  0, -5,
            -5,  0,  5,  5,  5,  5,  0, -5,
            -10,  0,  5,  5,  5,  5,  0,-10,
            -10,  0,  0,  0,  0,  0,  0,-10,
            -20,-10,-10, -5, -5,-10,-10,-20
        ]
        self.piece_square_table['K'] = [
            20, 30, 10,  0,  0, 10, 30, 20,
            20, 20,  0,  0,  0,  0, 20, 20,
            -10,-20,-20,-20,-20,-20,-20,-10,
            -20,-30,-30,-40,-40,-30,-30,-20,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
        ]
        self.piece_square_table['p']=self.piece_square_table['P'][::-1]
        self.piece_square_table['n']=self.piece_square_table['N'][::-1]
        self.piece_square_table['b']=self.piece_square_table['B'][::-1]
        self.piece_square_table['r']=self.piece_square_table['R'][::-1]
        self.piece_square_table['q']=self.piece_square_table['Q'][::-1]
        self.piece_square_table['k']=self.piece_square_table['K'][::-1]

    def get_piece_square_dict(self,fen):
        '''
        Takes FEN string corresponding to a position as input
        Returns a dictionary containing piece_symbols as keys and their
        respective positions on the board as a list of integers
        '''
        board=chess.Board(fen)
        piece_square_dict=defaultdict(list)
        for i in range(64):
            curr_piece=board.piece_at(i)
            if curr_piece:
                piece_square_dict[curr_piece.symbol()].append(i)
        return piece_square_dict

    def get_piece_value(self, piece_symbol):
        return self.B_piece_square_table(piece_symbol)

    def get_piece_eval(self, piece_symbol):
        white_eval=0
        for sq in self.piece_square_dict[piece_symbol.upper()]:
            white_eval+=self.piece_val[piece_symbol.upper()]+self.piece_square_table[piece_symbol.upper()][sq]
        black_eval=0
        for sq in self.piece_square_dict[piece_symbol.lower()]:
            black_eval+=self.piece_val[piece_symbol.lower()]+self.piece_square_table[piece_symbol.lower()][sq]
        return white_eval-black_eval
    
    def get_eval()
    
    
    def get_explanations(self):
        pieces=['p', 'b', 'n', 'r', 'q', 'k']
        piece_name={'p': 'Pawn(s)', 'n': 'Knight(s)', 'b': 'Bishop(s)', 'r': 'Rook(s)', 'q': 'Queen', 'k': 'King'}
        explanation_list=[]
        for piece in pieces:
            if self.get_psqt_eval(piece)>0:
                explanation_list.append(f"White's {piece_name[piece]} is/are placed at better square(s) than Black")
            elif self.get_psqt_eval(piece)<0:
                explanation_list.append(f"Black's {piece_name[piece]} is/are placed at better square(s) than White")
        return explanation_list
        


if __name__=='__main__':
    fen_str='rn2kb1r/pp2qppp/2p2n2/4p1B1/2B1P3/1QN5/PPP2PPP/R3K2R b KQkq - 1 9'
    psqt=PSQT(fen_str)
    # print(psqt.get_psqt_eval('p'))
    # print(psqt.get_psqt_eval('b'))
    # print(psqt.get_psqt_eval('n'))
    # print(psqt.get_psqt_eval('r'))
    # print(psqt.get_psqt_eval('q'))
    # print(psqt.get_psqt_eval('k'))
    exp_list=psqt.generate_explanation_list()
    for ex in exp_list:
        print(ex)


 
