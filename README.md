# Chess parser 

This parser uses Selenium to parse positions of chess figures from https://www.chess.com/ and make analysis of available moves.
And it also can automatically make the best moves in browser.

## Usage
- Run main_parse.py or main_parse_for_win.py (for windows) to just see analysis of current available moves when the hotkey is pressed.
- Run main_play.py or main_play_win.py (for windows) to automatically make the best moves.

## Requirements
- python >= 3.10
- [console-chess-imandyr](https://pypi.org/project/console-chess-imandyr/)
- [selenium](https://pypi.org/project/selenium/)
- [pynput](https://pypi.org/project/pynput/)
- [pytest](https://pypi.org/project/pytest/)