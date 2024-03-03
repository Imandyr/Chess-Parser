from parsing_functions import chess_com_universal_parser
from main_play import run_with_autoplay


if __name__ == "__main__":
    url = "https://www.chess.com/play/computer/arthur-the-adequate"
    start_hotkey = "a"
    stop_hotkey = "o"
    parse_func = chess_com_universal_parser
    username = input("www.chess.com username: ")
    password = input("www.chess.com password: ")
    run_with_autoplay(url, start_hotkey, stop_hotkey, username, password, parse_func)