# python-chessx
A chess XAI program

![Tests](https://github.com/abhinav7sinha/python-chessx/actions/workflows/tests.yml/badge.svg)
![GitHub last commit](https://img.shields.io/github/last-commit/abhinav7sinha/python-chessx)


1. [Introduction](#introduction)
2. [Dependencies](#dependencies)
3. [Features](#features)

## 1. Introduction<a name="introduction"/>
python-chessx is an explainable chess AI that generates commentary for positions/moves in a game of chess.

## 2. Dependencies<a name="dependencies"/>

* Python3 - [Download and Install Python3](https://www.python.org/downloads/). You can also use your system's package manager to install the latest stable version of python3.
* For dev work, run the following commands (preferrably in a virtual environment):
```bash
pip install -e .
```

## 3. Features<a name="features"/>

* Provides a utility to generate explanations from a FEN representation of a chess position based on Piece Square Tables
  ```python
  import chessx.psqt as psqt

  fen_str='rn2kb1r/pp2qppp/2p2n2/4p1B1/2B1P3/1QN5/PPP2PPP/R3K2R b KQkq - 1 9'
  psqt_util=psqt.PSQT(fen_str)

  # generate list of explanations
  exp_list=psqt_util.get_explanations()

  # print explanations
  print('PSQT Explanations:')
  for exp in exp_list:
      print(exp)
  ```