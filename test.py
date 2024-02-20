# python3 -m pytest 14.5/chess_parser/test.py


import pytest
from console_chess_imandyr.bot import Move

from parsing import truncate_moves


def test_truncate_moves() -> None:
    fake_moves = [Move(None, None, None, 1)]
    t = truncate_moves(fake_moves)
    assert t == fake_moves


def test_2():
    pass

