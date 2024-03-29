from dataclasses import dataclass
from typing import Callable, Optional, TypedDict, Iterable
import re

from selenium.common import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from console_chess_imandyr.base import Table, Player, Figure
from console_chess_imandyr.bot import Bot, HardBot, Move
from console_chess_imandyr.game import ChessSet
from console_chess_imandyr.figures import Pawn, Rook, Knight, Bishop, Queen, King


class ChessNotFound(ValueError):
    """ Can be raised if parse_function did not find any chess figures on the page. """


class AuthorizationError(ValueError):
    """ Can be raised if the authorization function fails. """


@dataclass
class ChessSetBot:
    """ Dataclass object which contains a table and two bots. """
    table: Optional[Table] = None
    player_white: Optional[Bot] = None
    player_black: Optional[Bot] = None

    def __post_init__(self) -> None:
        self.table = self.table or Table(8, 8)
        self.player_white = self.player_white or HardBot(self.table, True, "White")
        self.player_black = self.player_black or HardBot(self.table, False, "Black")


authorization_function = Callable[[WebDriver], None]
parse_function = Callable[[WebDriver], ChessSetBot]
output_function = Callable[[Iterable[Move]], str]


figure_pattern = re.compile(r"piece (?P<color>\w)(?P<piece>\w) square-(?P<column>\d)(?P<row>\d)")
piece_dict = {"r": Rook, "n": Knight, "b": Bishop, "k": King, "q": Queen, "p": Pawn, "f": Figure}
piece_dict_rev = {v: k for k, v in piece_dict.items()}


class FigureDict(TypedDict):
    color: str
    piece: str
    column: str
    row: str


def tune_pawns(table: Table) -> None:
    """
    Takes table with figures and changes first_move attribute in all pawns to value that it must really be now.
    :param table: Table with figures.
    :return: None, all changes will be done to the given table.
    """
    for f in table.figures:
        if isinstance(f, Pawn):
            p = f.position
            if p[0] in {1, 6}:
                f.first_move = True
            else:
                f.first_move = False


class ChessComTableParser:
    def __init__(self, xpath: str, doc: str) -> None:
        """
        Creates a parser object, which will parse figures from the page of https://www.chess.com/
        on call, using xpath given on initialization.
        :param xpath: Xpath string by which page elements with figures properties will be selected.
        :param doc: Docstring of a newly created object.
        """
        self.xpath = xpath
        self.__doc__ = doc
        self._driver: Optional[WebDriver] = None

    def _create_game_set(self) -> ChessSetBot:
        """ Creates a game set with table, white and black players. """
        table = Table()
        white, black = HardBot(table, True, "White"), HardBot(table, False, "Black")
        return ChessSetBot(table, white, black)

    def __call__(self, driver: WebDriver) -> ChessSetBot:
        """ Parses chess figures and positions from the currently opened page from https://www.chess.com/
        into ChessSetBot. """
        self._driver = driver
        chess_set = self._create_game_set()

        for figure in driver.find_elements(By.XPATH, self.xpath):
            if (figure := figure_pattern.match(figure.get_attribute("class"))) is not None:
                figure = figure.groupdict()
                chess_set.table.set_figure(piece_dict[figure["piece"]](chess_set.table,
                                                                       chess_set.player_white
                                                                       if figure["color"] == "w"
                                                                       else chess_set.player_black),
                                           (8 - int(figure["row"]), int(figure["column"]) - 1))
        if len(chess_set.table.figures) == 0:
            raise ChessNotFound("The parsing function did not find any chess figures on the page.")
        tune_pawns(chess_set.table)
        return chess_set


chess_com_bot_parse = ChessComTableParser(
    '//*[@id="board-play-computer"]/div',
    " Parses chess figures and positions from the currently opened page from https://www.chess.com/ "
    "when playing against bot. "
)


# class ChessComTableParserPvP(ChessComTableParser):
#     def _create_game_set(self) -> ChessSetBot:
#         """ Creates a game set with table, white and black players. With respect to player color. """
#         table = Table()
#         player_c = self._driver.find_element(
#             By.XPATH,
#             '//*[@id="board-layout-player-bottom"]/div/div[2]/wc-captured-pieces'
#         ).get_attribute("player-color")
#         if player_c == 2:
#             white, black = HardBot(table, False, "White"), HardBot(table, True, "Black")
#         else:
#             white, black = HardBot(table, True, "White"), HardBot(table, False, "Black")
#         return ChessSetBot(table, white, black)


chess_com_pvp_parse = ChessComTableParser(
    '//*[@id="board-single"]/div',
    " Parses chess figures and positions from the currently opened page from https://www.chess.com/ "
    "when playing against player. "
)


def chess_com_universal_parser(driver: WebDriver) -> ChessSetBot:
    """ Universal parser, which can parse both PvP and PvB. """
    try:
        return chess_com_pvp_parse(driver)
    except (WebDriverException, ChessNotFound):
        return chess_com_bot_parse(driver)


def chess_com_authorization(driver: WebDriver, username: str, password: str) -> None:
    """ Authorizes on https://www.chess.com/ using given username and password. """
    prev_url = driver.current_url
    login_url = "https://www.chess.com/login_and_go?"
    driver.get(login_url)
    driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(username)
    driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(password)
    driver.find_element(By.XPATH, '//*[@id="login"]').click()
    if driver.current_url == login_url:
        raise AuthorizationError("Authorization to www.chess.com failed.")
    driver.get(prev_url)


def to_chess_com(position: tuple[int, int]) -> tuple[int, int]:
    """ Converts position values from console_chess_imandyr format into https://www.chess.com/ format. """
    return 8 - position[0], position[1] + 1


def chess_com_moves_output(moves: Iterable[Move]) -> str:
    """ Converts a list of figure moves into appropriate for https://www.chess.com/ string representation."""
    return " ; ".join(f"{move.figure}{to_chess_com(move.figure.position)} -> "
                      f"{move.content}{to_chess_com(move.to)} == {move.cost}" for move in moves)
