from time import sleep
from typing import Optional, Callable
from abc import ABC, abstractmethod

from console_chess_imandyr.base import Figure
from console_chess_imandyr.bot import Move
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException

from parsing import ChessParser, add_content
from parsing_functions import to_chess_com, chess_com_moves_output, piece_dict_rev


class ChessPlayer(ABC):
    def __init__(self, parser: Optional[ChessParser] = None) -> None:
        """
        Chess player is making moves in webpage opened in parser. Call .move() method to make move.
        :param parser: ChessParser object which will open a webpage with chess game and parse it.
        """
        self.autoplay: bool = False
        if parser is None:
            parser = ChessParser()
        self.parser = parser

    def get_best_move(self) -> Move:
        """ Returns best possible move. """
        chess_set = self.parser.use_parse_func()
        try:
            player_c = self.parser.driver.find_element(
                By.XPATH, '//*[@id="board-layout-player-bottom"]/div/div[2]/wc-captured-pieces'
            ).get_attribute("player-color")
            if player_c == "2":
                best = chess_set.player_black.best_move
            else:
                best = chess_set.player_white.best_move
        except WebDriverException:
            best = chess_set.player_white.best_move
        best = add_content(chess_set.table, best)
        return best

    @abstractmethod
    def make_move(self) -> Move:
        """ Implementation-specific move-making method. Must return made Move. """

    def move(self) -> None:
        """ Makes one move. """
        print(chess_com_moves_output([self.make_move()]))

    def eternal_movement(self, interval: float) -> None:
        """
        Endlessly calls .move() every interval while "self.autoplay" is True.
        :param interval: Waiting interval.
        :return: None
        """
        self.autoplay = True
        while self.autoplay:
            self.move()
            sleep(interval)


class ChessComPlayer(ChessPlayer):
    def make_move(self) -> Move:
        """
        Makes the best possible move in the currently opened chess game and returns it.
        :return: The best move in Move object.
        """
        move = self.get_best_move()
        try:
            figure_el = chess_com_element(move.figure)
            if move.content is None:
                to_el = chess_com_hint_square(move.to)
            else:
                to_el = chess_com_element(move.content)
            figure_el = self.parser.driver.find_element(By.XPATH, f'//*[@class="{figure_el}"]')
            figure_el.click()
            to_el = self.parser.driver.find_element(By.XPATH, f'//*[@class="{to_el}"]')
            ActionChains(self.parser.driver).drag_and_drop(figure_el, to_el).perform()
        except WebDriverException:
            print("An exception occurred when a player tried to make a move.")
        return move


def tuple_to_str(t: tuple) -> str:
    return ''.join(map(str, t))


def chess_com_element(figure: Figure) -> str:
    """
    Converts given Figure into the name of the element class from https://www.chess.com/.
    :param figure: Figure object.
    :return: String representation.
    """
    return (f"piece {figure.player.name[0].lower()}{piece_dict_rev[type(figure)]} "
            f"square-{tuple_to_str(to_chess_com(figure.position)[::-1])}")


def chess_com_hint_square(position: tuple[int, int]) -> str:
    """ Converts position to https://www.chess.com/ hint square element class name. """
    return f"hint square-{tuple_to_str(to_chess_com(position)[::-1])}"
