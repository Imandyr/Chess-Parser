from typing import Optional, Callable
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from console_chess_imandyr.game import ChessSet
from console_chess_imandyr.bot import Move

from parsing_functions import (parse_function, authorization_function, output_function, chess_com_bot_parse,
                               chess_com_moves_output, ChessNotFound, AuthorizationError)


def truncate_moves(moves: list[Move], n_best: int = 3, n_worst: int = 3) -> list[Move]:
    """ Return n_best and n_worst moves from a list of moves. """
    moves.sort(key=lambda x: x.cost, reverse=True)
    if len(moves) <= n_best + n_worst:
        return moves
    output = moves[:n_best]
    output.extend(moves[-n_worst:])
    return output


class ChessParser:
    def __init__(self, url: str = "https://www.chess.com/", driver: Optional[WebDriver] = None,
                 n_best: int = 3, n_worst: int = 3,
                 authorization: Optional[authorization_function] = None,
                 parse_func: Optional[parse_function] = None,
                 output_func: Optional[output_function] = None) -> None:
        """
        Chess parser class is used to open a given url in a driver, parse it on call of .parse() method using parse_func
        and then print the analysis of this chess situation.

        :param url: URL to the target website with chess game on it.
        :param driver: Selenium WebDriver instance through which this website will be used.
        :param n_best: Number of the best possible moves which will be displayed on parse.
        :param n_worst: Number of the worst possible moves which will be displayed on parse.
        :param authorization: Function for authorization on target website. Authorize if provided and
         do nothing if None.
        :param parse_func: Function which will be used to parse the current page opened in WebDriver
         to get chess figures and their positions, transforming them into ChessSet object for further analysis.
        :param output_func: The function which will be used to convert a list with figures moves into
        some string representation, which will be printed after parsing.
        """
        self.url, self.authorization, self.n_best, self.n_worst = url, authorization, n_best, n_worst
        if driver is None:
            driver = webdriver.Chrome()
        self.driver = driver
        if parse_func is None:
            parse_func = chess_com_bot_parse
        self.parse_func = parse_func
        if output_func is None:
            output_func = chess_com_moves_output
        self.output_func = output_func
        self._start()

    def _start(self) -> None:
        """ Opens url in a driver and authorize on website. """
        self.driver.get(self.url)
        if self.authorization:
            try:
                self.authorization(self.driver)
                print("Authorization to www.chess.com was successful.")
            except AuthorizationError as err:
                print(err)

    def parse(self, parse_func: Optional[parse_function] = None) -> None:
        """
        Parses currently opened page using self.parse_func or given parse_func and prints analysis of
         the current game state.

        :param parse_func: Function which will be used instead of current self.parse_func if specified.
        :return: None
        """
        parse_func = parse_func or self.parse_func
        try:
            chess_set = parse_func(self.driver)
            white_moves = truncate_moves(chess_set.player_white.available_moves_costs, self.n_best, self.n_worst)
            black_moves = truncate_moves(chess_set.player_black.available_moves_costs, self.n_best, self.n_worst)
            print(f"White's moves costs: {self.output_func(white_moves)}\n"
                  f"Black's moves costs: {self.output_func(black_moves)}")
        except ChessNotFound as err:
            print(err)

