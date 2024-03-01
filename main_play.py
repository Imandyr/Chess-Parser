import threading
from typing import Callable

from pynput.keyboard import HotKey, Listener
from selenium.webdriver.remote.webdriver import WebDriver

from parsing import ChessParser
from parsing_functions import (chess_com_authorization, chess_com_pvp_parse, chess_com_bot_parse,
                               chess_com_universal_parser)
from player import ChessComPlayer


def create_hotkey(key: str, func: Callable) -> Listener:
    start = HotKey(HotKey.parse(key), func)
    start_listener = Listener(on_press=start.press, on_release=start.release)
    return start_listener


def run(url: str, move_hotkey: str, username: str, password: str, parse_func=chess_com_universal_parser) -> None:

    def auth(driver: WebDriver) -> None:
        chess_com_authorization(driver, username, password)

    chess_player = ChessComPlayer(ChessParser(url, parse_func=parse_func, authorization=auth))

    listener = create_hotkey(move_hotkey, chess_player.move)
    listener.start()

    # Waits forever for listener to end
    listener.join()


def run_with_autoplay(url: str, start_hotkey: str, stop_hotkey: str, username: str, password: str,
                      parse_func=chess_com_universal_parser) -> None:

    def auth(driver: WebDriver) -> None:
        chess_com_authorization(driver, username, password)

    chess_player = ChessComPlayer(ChessParser(url, parse_func=parse_func, authorization=auth))

    def start_autoplay() -> None:
        autoplay = threading.Thread(target=chess_player.eternal_movement, args=(5,))
        autoplay.start()

    start_listener = create_hotkey(start_hotkey, start_autoplay)
    start_listener.start()

    stop_listener = create_hotkey(stop_hotkey, lambda: setattr(chess_player, "autoplay", False))
    stop_listener.start()

    stop_listener.join()


if __name__ == "__main__":
    url = "https://www.chess.com/play/computer/arthur-the-adequate"
    start_hotkey = "<ctrl>+<alt>+a"
    stop_hotkey = "<ctrl>+<alt>+o"
    parse_func = chess_com_universal_parser
    # username = input("www.chess.com username: ")
    # password = input("www.chess.com password: ")
    username = "UnstableGamer282"
    password = "o30klvolikn40IfnMzZoe93uchf"
    run_with_autoplay(url, start_hotkey, stop_hotkey, username, password, parse_func)

    # url = "https://www.chess.com/play/computer/arthur-the-adequate"
    # hotkey = "<ctrl>+<alt>+p"
    # parse_func = chess_com_universal_parser
    # # username = input("www.chess.com username: ")
    # # password = input("www.chess.com password: ")
    # username = "UnstableGamer282"
    # password = "o30klvolikn40IfnMzZoe93uchf"
    # run(url, hotkey, username, password, parse_func)



