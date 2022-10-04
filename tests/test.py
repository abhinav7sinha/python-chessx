import unittest
import chessx.heuristic as heuristic


class TestPSQT(unittest.TestCase):
    def test_psqt_map(self):
        '''
        Test Piece Square Tables for each piece
        '''
        fen_str = 'rn2kb1r/pp2qppp/2p2n2/4p1B1/2B1P3/1QN5/PPP2PPP/R3K2R b KQkq - 1 9'
        psqt_util = heuristic.PSQT(fen_str)

        psqt_map = psqt_util.psqt_map

        # PSQT map has 12 keys -> corresponding to piece types for each color
        self.assertEqual(len(psqt_map), 12)

        # each key has a PSQT array of size 64
        for k in psqt_map.keys():
            self.assertEqual(len(psqt_map[k]), 64)

    def test_explanations(self):
        '''
        Test PSQT explanations
        '''
        fen_str_1 = 'rn2kb1r/pp2qppp/2p2n2/4p1B1/2B1P3/1QN5/PPP2PPP/R3K2R b KQkq - 1 9'
        psqt_util = heuristic.PSQT(fen_str_1)

        exp_list = psqt_util.get_explanations()

        # fen_str_1 should generate 4 PSQT explanation strings
        self.assertEqual(len(exp_list), 4)


if __name__ == '__main__':
    unittest.main()
