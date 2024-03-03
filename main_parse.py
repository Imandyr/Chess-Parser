from pynput.keyboard import HotKey, Listener
from selenium.webdriver.remote.webdriver import WebDriver

from parsing import ChessParser
from parsing_functions import chess_com_authorization, chess_com_pvp_parse, chess_com_bot_parse, chess_com_universal_parser


def run(url: str, parse_hotkey: str, username: str, password: str, parse_func=chess_com_universal_parser) -> None:

    def auth(driver: WebDriver) -> None:
        chess_com_authorization(driver, username, password)

    chess_parser = ChessParser(url, parse_func=parse_func, authorization=auth)

    hotkey = HotKey(HotKey.parse(parse_hotkey), chess_parser.parse)
    listener = Listener(on_press=hotkey.press, on_release=hotkey.release)
    listener.start()

    # Waits forever for listener to end
    listener.join()


if __name__ == "__main__":
    url = "https://www.chess.com/play/computer/arthur-the-adequate"
    parse_hotkey = "<ctrl>+<alt>+p"
    parse_func = chess_com_universal_parser
    username = input("www.chess.com username: ")
    password = input("www.chess.com password: ")
    run(url, parse_hotkey, username, password, parse_func)



