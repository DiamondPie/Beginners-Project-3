import curses, time
from typing import Optional

def typing(stdscr: curses.window, y: Optional[int], x: Optional[int], text: "str | 'list[str]'", color, delay=0.01):
    relative_pos = y is None and x is None
    if type(text) == str:
        flag = 0
        for char in text:
            if char == '\n':
                flag = 0
                y += 1
                continue
            if relative_pos:
                stdscr.addstr(char, color)
            else:
                stdscr.addstr(y, x+flag, char, color)
            stdscr.refresh()
            time.sleep(delay)
            flag += 1
    elif type(text) == list:
        for line in text:
            typing(stdscr, y, x, line, color, delay)
            y += 1

def typing_reversely(stdscr: curses.window, y: int, x: int, text: "str | 'list[str]'", color, delay=0.01):
    if type(text) == str:
        flag = len(text)
        for char in reversed(text):
            if char == '\n':
                flag = len(text)
                y += 1
                continue
            else:
                stdscr.addstr(y, x+flag, char, color)
            stdscr.refresh()
            time.sleep(delay)
            flag -= 1
    elif type(text) == list:
        for line in text:
            typing(stdscr, y, x, line, color, delay)
            y += 1
