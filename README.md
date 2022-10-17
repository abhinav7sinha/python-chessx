# python-chessx
A chess XAI program

![Tests](https://github.com/abhinav7sinha/python-chessx/actions/workflows/tests.yml/badge.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/chessx)
![PyPI](https://img.shields.io/pypi/v/chessx)
![GitHub last commit](https://img.shields.io/github/last-commit/abhinav7sinha/python-chessx)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/chessx)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/chess)


1. [Introduction](#introduction)
2. [Dependencies](#dependencies)
3. [Features](#features)
4. [Tests](#tests)

## 1. Introduction<a name="introduction"/>
python-chessx is an explainable chess AI that generates commentary for positions/moves in a game of chess.

## 2. Dependencies<a name="dependencies"/>

* Python3 - [Download and Install Python3](https://www.python.org/downloads/). You can also use your system's package manager to install the latest stable version of python3.
* For dev work, run the following commands (preferrably in a virtual environment):
```bash
pip install -e .
```

## 3. Features<a name="features"/>

* Provides a utility to generate explanations from a FEN representation of a chess position.
  1. Piece Square Tables
  ```python
  import chessx.heuristic as heuristic
  import chess

  psqt_fen = 'rn2kb1r/pp2qppp/2p2n2/4p1B1/2B1P3/1QN5/PPP2PPP/R3K2R b KQkq - 1 9'
  psqt_util=heuristic.PSQT(psqt_fen)

  # generate list of explanations
  exp_list=psqt_util.get_explanations()

  # print explanations
  print('PSQT Explanations:')
  for exp in exp_list:
      print(exp)
  ```
  2. Trapped Pieces
  ```python
  tp_fen='r5k1/p4p1p/2p3pb/2N1n2n/1p2PP2/1B2B1PP/PP4K1/3R4 b - - 0 24'
  tp_util=heuristic.TrappedPieces(tp_fen)

  # generate list of explanations
  exp_list=tp_util.get_explanations()

  # print explanations
  print('Trapped Pieces Explanations:')
  for exp in exp_list:
      print(exp)
  ```
  3. Pinned Pieces
  ```python
  pin_fen='1rk5/8/4n3/5B2/1N6/8/8/1Q1K4 b - - 0 1'
  pin_util=heuristic.PinnedPieces(pin_fen)

  # generate list of explanations
  exp_list = pin_util.get_explanations()

  # print explanations
  print('PinnedPieces Explanations:')
  for ex in exp_list:
      print(ex)  
  print()
  ``` 

## 3. Tests<a name="tests"/>
The following command to runs unit tests on the project:
```bash
pytest
  ```
