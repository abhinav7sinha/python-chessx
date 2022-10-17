from __future__ import annotations
from collections import defaultdict
from typing import Dict, List
from abc import ABC, abstractmethod
import chess

class Heuristic(ABC):
    @abstractmethod
    def get_explanations(self) -> List[str]:
        pass


class PinnedPieceType:
    def __init__(self, piece_sq: int, pinned_to_sq: int, pinned_by_sq: int) -> None:
        self.piece_sq = piece_sq
        self.pinned_to_sq = pinned_to_sq
        self.pinned_by_sq = pinned_by_sq
    
    def __str__(self):
        return (f'piece_sq: {self.piece_sq}, pinned_to_sq: {self.pinned_to_sq}, pinned_by_sq: {self.pinned_by_sq}')


class PinnedPieces:
    '''
    a pin is a chess tactic in which a defending piece cannot move without exposing a more 
    valuable defending piece on its other side to capture by the attacking piece
    '''

    def __init__(self, fen: str) -> None:
        self.fen = fen
        self.board = chess.Board(self.fen)
        self.piece_name = {'p': 'Pawn', 'n': 'Knight', 'b': 'Bishop', 'r': 'Rook', 'q': 'Queen', 'k': 'King'}
        self.piece_val_map = {
            'p': 1, 'n': 3, 'b': 3, 'r': 5, 'q': 9, 'k': 200
        }

    def get_pinned_pieces(self):
        pass

    def get_absolute_pins(self) -> List(PinnedPieceType):
        '''
        An absolute pin is one where the piece shielded by the pinned piece is the king.
        '''
        pinned_pieces=[]
        colors=[chess.BLACK, chess.WHITE]
        for color in colors:
            for sq in range(64):
                if self.board.is_pinned(color, sq):
                    pinned_piece=PinnedPieceType(piece_sq=sq, pinned_to_sq=self.board.king(color), pinned_by_sq=-1)
                    potential_pinned_by_sqs=[]
                    for sq2 in self.board.pin(color, sq):
                        if self.board.color_at(sq2) is not None and self.board.color_at(sq2) is not color and self.board.piece_at(sq2).symbol().lower()!='p':
                            potential_pinned_by_sqs.append(sq2)
                    if len(potential_pinned_by_sqs)==1:
                        pinned_piece.pinned_by_sq=potential_pinned_by_sqs[0]
                    else:
                        base_dist=self.board.king(color)-sq
                        min_dist=64
                        for i in range(len(potential_pinned_by_sqs)):
                            if base_dist>0:
                                if sq-potential_pinned_by_sqs[i]>0 and sq-potential_pinned_by_sqs[i]<min_dist:
                                    pinned_piece.pinned_by_sq=potential_pinned_by_sqs[i]
                                    min_dist=sq-potential_pinned_by_sqs[i]
                            else:
                                if sq-potential_pinned_by_sqs[i]<0 and potential_pinned_by_sqs[i]-sq<min_dist:
                                    pinned_piece.pinned_by_sq=potential_pinned_by_sqs[i]
                                    min_dist=potential_pinned_by_sqs[i]-sq
                    pinned_pieces.append(pinned_piece)
        return pinned_pieces


    def get_explanations(self) -> List[str]:
        '''
        Returns list of explanations corresponding to each pinned piece
        '''
        pinned_pieces = self.get_absolute_pins()
        explanation_list = []
        for piece in pinned_pieces:
            color='White' if self.board.color_at(piece.piece_sq) is True else 'Black'
            explanation_list.append(f'{color} {self.piece_name[self.board.piece_at(piece.piece_sq).symbol().lower()]} '\
                f'at {chess.square_name(piece.piece_sq)} is pinned to its '
                f'{self.piece_name[self.board.piece_at(piece.pinned_to_sq).symbol().lower()]} '
                f'at {chess.square_name(piece.pinned_to_sq)} by the opponent\'s '
                f'{self.piece_name[self.board.piece_at(piece.pinned_by_sq).symbol().lower()]} '
                f'at {chess.square_name(piece.pinned_by_sq)}')
        return explanation_list      

class TrappedPieces:
    '''
    if all squares that a piece can go to are controlled by the opponent, then the piece is trapped.
    '''
    def __init__(self, fen: str) -> None:
        self.fen = fen
        self.board = chess.Board(self.fen)
        self.piece_name = {'p': 'Pawn(s)', 'n': 'Knight(s)', 'b': 'Bishop(s)', 'r': 'Rook(s)', 'q': 'Queen', 'k': 'King'}
        self.piece_val_map = {
            'p': 1, 'n': 3, 'b': 3, 'r': 5, 'q': 9, 'k': 200
        }

    def check_en_prise(self, from_sq: int, to_sq: int) -> bool:
        curr_piece=self.board.piece_at(from_sq)
        curr_color=self.board.color_at(from_sq)
        curr_piece_val=self.piece_val_map[curr_piece.symbol().lower()]
        tboard=chess.Board(self.fen)
        tboard.push(chess.Move(from_square=from_sq, to_square=to_sq))
        
        defenders=tboard.attackers(curr_color, to_sq)
        attackers=tboard.attackers(not curr_color, to_sq)

        len_a=len(attackers)
        len_d=len(defenders)

        # if there are no defenders but there are attackers then return True
        if len_a>0 and len_d==0:
            return True
        
        if len_a==0:
            return False

        # If any of the attackers have lower piece val than that of curr_piece,
        # return True
        for att_piece in attackers:
            if self.piece_val_map[tboard.piece_at(att_piece).symbol().lower()]<curr_piece_val:
                return True
        
        attackers_val=[self.piece_val_map[tboard.piece_at(att_piece).symbol().lower()] for att_piece in attackers]
        attackers_val=sorted(attackers_val)
        defenders_val=[self.piece_val_map[tboard.piece_at(def_piece).symbol().lower()] for def_piece in defenders]
        defenders_val=sorted(defenders_val)
        a=0
        d=0
        score=0
        temp=curr_piece_val
        while a<len_a and d<len_d:
            if attackers_val[a]<defenders_val[d] and score<=0:
                return False
            else:
                score+=temp-attackers_val[a]
                temp=defenders_val[d]
                a+=1
                d+=1
        if len_a>len_d:
            score+=temp-attackers_val[a]
            if score<=0:
                return False
            else:
                return True
        elif score<=0:
            return False
        else:
            return True


    def get_trapped_pieces(self) -> Dict[str, List[int]]:
        '''
        Returns list of all trapped pieces in a position
        '''
        trapped_pieces=defaultdict(list)
        for i in range(64):
            if self.board.piece_at(i)!=None and self.board.piece_at(i).piece_type>1 and self.is_trapped(i):
                trapped_pieces[self.board.piece_at(i).symbol()].append(i)
        return trapped_pieces

    def is_trapped(self, curr_sq: int) -> bool:
        '''
        Returns True if piece at the given input square is trapped,
        else Returns False
        '''
        # get list of all possible squares that the current piece can go to
        possible_squares=[]
        curr_col=self.board.color_at(curr_sq)
        for sq in self.board.attacks(curr_sq):
            if self.board.piece_at(sq) != None and self.board.piece_at(sq).color is curr_col:
                continue
            possible_squares.append(sq)
        
        # if the piece is not attacking any sqaures -> then check if 
        # it's at it's starting square -> in that case -> it's not trapped
        if len(possible_squares)==0:
            if curr_sq==0 and self.board.piece_at(curr_sq).symbol()=='R':
                return False
            elif curr_sq==2 and self.board.piece_at(curr_sq).symbol()=='B':
                return False
            elif curr_sq==5 and self.board.piece_at(curr_sq).symbol()=='B':
                return False
            elif curr_sq==7 and self.board.piece_at(curr_sq).symbol()=='R':
                return False
            elif curr_sq==56 and self.board.piece_at(curr_sq).symbol()=='r':
                return False
            elif curr_sq==58 and self.board.piece_at(curr_sq).symbol()=='b':
                return False
            elif curr_sq==61 and self.board.piece_at(curr_sq).symbol()=='b':
                return False
            elif curr_sq==63 and self.board.piece_at(curr_sq).symbol()=='r':
                return False

        # Check if all these possible squares are defended by the opposite side
        num_possible_sqs=len(possible_squares)
        num_defended_sqs=0
        # for sq in possible_squares:
        #     # get attackers of the possible squares
        #     attacker_sqs=self.board.attackers(not curr_col, sq)
        #     for a_sq in attacker_sqs:
        #         if self.piece_val_map[self.board.piece_at(a_sq).symbol().lower()] < \
        #             self.piece_val_map[self.board.piece_at(curr_sq).symbol().lower()]:
        #             num_defended_sqs+=1
        #             break
        for sq in possible_squares:
            if self.check_en_prise(from_sq=curr_sq, to_sq=sq):
                num_defended_sqs+=1

        if num_possible_sqs-num_defended_sqs==0:
            return True
        else:
            return False

    def get_explanations(self) -> List[str]:
        '''
        Returns list of explanations corresponding to each trapped piece
        '''
        trapped_pieces=self.get_trapped_pieces()
        explanation_list = []
        for piece in trapped_pieces:
            color='White' if piece.isupper() else 'Black'
            for square in trapped_pieces[piece]:
                sq=chess.square_name(square)
                explanation_list.append(f'{color} {self.piece_name[piece.lower()]} at {sq} is trapped')
        return explanation_list
        

class Mobility:
    '''
    Class containing logic to evaluate Mobility of Pieces
    '''

    def __init__(self, fen: str) -> None:
        self.fen = fen
    


# TODO: PeSTO's Evaluation Function
class PSQT(Heuristic):
    '''
    Class containing logic for Piece Square Tables
    '''

    def __init__(self, fen: str) -> None:
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
    psqt_fen = 'rn2kb1r/pp2qppp/2p2n2/4p1B1/2B1P3/1QN5/PPP2PPP/R3K2R b KQkq - 1 9'
    psqt = PSQT(psqt_fen)
    exp_list = psqt.get_explanations()
    print('PSQT Explanations:')
    for ex in exp_list:
        print(ex)
    print()

    tp_fen='r5k1/p4p1p/2p3pb/2N1n2n/1p2PP2/1B2B1PP/PP4K1/3R4 b - - 0 24'
    # tp = TrappedPieces('rn1qk1nr/pppppppp/6b1/5P1P/6P1/8/PPPP4/RNBQKBNR w KQkq - 0 1')
    tp=TrappedPieces(tp_fen)
    exp_list = tp.get_explanations()
    print('TrappedPieces Explanations:')
    for ex in exp_list:
        print(ex)   
    print()
    
    pin_fen='1rk5/8/4n3/5B2/1N6/8/8/1Q1K4 b - - 0 1'
    pin=PinnedPieces(pin_fen)
    exp_list = pin.get_explanations()
    print('PinnedPieces Explanations:')
    for ex in exp_list:
        print(ex)  
    print() 