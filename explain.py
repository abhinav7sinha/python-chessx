import os
os.system('cls' if os.name == 'nt' else 'clear')

import chess

class PositionXAI:
    def __init__(self, fen):
        self.fen=fen
        self.board=chess.Board(fen)
    
    def generate_explanations(self):
        '''
        generate all explanations for the current position
        '''
        pass