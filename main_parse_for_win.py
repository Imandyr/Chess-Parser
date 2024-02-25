

from parsing_functions import chess_com_pvp_parse, chess_com_bot_parse
from main_parse import run


if __name__ == "__main__":
    url = "https://www.chess.com/play/computer/arthur-the-adequate"
    parse_hotkey = "p"
    parse_func = chess_com_bot_parse
    # username = input("www.chess.com username: ")
    # password = input("www.chess.com password: ")
    username = "UnstableGamer282"
    password = "o30klvolikn40IfnMzZoe93uchf"
    run(url, parse_hotkey, username, password, parse_func)
