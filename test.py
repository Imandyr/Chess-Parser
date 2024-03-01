import pytest
from console_chess_imandyr.bot import Move
from console_chess_imandyr.base import Table, Player
from console_chess_imandyr.figures import Queen, Pawn

from parsing_functions import to_chess_com, tune_pawns
from player import chess_com_hint_square, chess_com_element


@pytest.fixture
def table_player_queen() -> tuple[Table, Player, Queen]:
    t = Table()
    p = Player(t, True, "Black")
    q = Queen(t, p)
    t.set_figure(q, (3, 4))
    return t, p, q


# def test_truncate_moves() -> None:
#     fake_moves = [Move(None, None, None, 1)]
#     t = truncate_moves(fake_moves)
#     assert t == fake_moves


def test_to_chess_com() -> None:
    assert to_chess_com((6, 2)) == (2, 3)


def test_chess_com_element(table_player_queen) -> None:
    t, p, q = table_player_queen
    assert chess_com_element(q) == "piece bq square-55"


def test_chess_com_hint_square(table_player_queen) -> None:
    t, p, q = table_player_queen
    assert chess_com_hint_square(q.position) == "hint square-55"


def test_tune_paws() -> None:
    t = Table()
    p = Player(t, True, "Black")
    pa1, pa2, pa3 = Pawn(t, p), Pawn(t, p), Pawn(t, p)
    t.set_figure(pa1, (1, 3)); t.set_figure(pa2, (6, 7)); t.set_figure(pa3, (2, 5))
    tune_pawns(t)
    assert pa1.first_move and pa2.first_move and not pa3.first_move

