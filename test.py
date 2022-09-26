import explain

fen_str='rn2kb1r/pp2qppp/2p2n2/4p1B1/2B1P3/1QN5/PPP2PPP/R3K2R b KQkq - 1 9'

# create PostionXAI object
position=explain.PositionXAI(fen_str)

# generate explanations
explanations_list=position.generate_explanations()
