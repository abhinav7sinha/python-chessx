import psqt # assumes you have psqt.py in the same directory, or you know how to handle python modules.

fen_str='rn2kb1r/pp2qppp/2p2n2/4p1B1/2B1P3/1QN5/PPP2PPP/R3K2R b KQkq - 1 9'
psqt_util=psqt.PSQT(fen_str)

# generate list of explanations
exp_list=psqt_util.get_explanations()

# print explanations
print('PSQT Explanations:')
for exp in exp_list:
    print(exp)