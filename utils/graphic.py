import curses, random, time
from typing import Literal

def flame(stdscr: curses.window, y, x, height, width, color, style:Literal["normal", "bold", "round", "double"]="normal", fill=False):
    if style == "bold":
        flame_angles = ('┏', '┓', '┗', '┛')
        flame_lines = ('━', '┃')
    elif style == "round":
        flame_angles = ('╭', '╮', '╰', '╯')
        flame_lines = ('─', '│')
    elif style == "double":
        flame_angles = ('╔', '╗', '╚', '╝')
        flame_lines = ('═', '║')
    else:
        flame_angles = ('┌', '┐', '└', '┘')
        flame_lines = ('─', '│')

    stdscr.addstr(y, x, flame_angles[0]+flame_lines[0]*(width-2)+flame_angles[1], color)
    stdscr.addstr(y+height-1, x, flame_angles[2]+flame_lines[0]*(width-2)+flame_angles[3], color)
    for i in range(y+1, y+height-1):
        stdscr.addstr(i, x, flame_lines[1], color)
        if fill: stdscr.addstr(i, x+1, ' '*(width-2), color)
        stdscr.addstr(i, x+width-1, flame_lines[1], color)

def clear_screen_randomly(stdscr: curses.window, loop_times=20, in_sec=2):
    height, width = stdscr.getmaxyx()
    
    positions = [(y, x) for y in range(height) for x in range(width)]
    
    random.shuffle(positions)
    
    total_positions = len(positions)
    positions_per_second = total_positions // loop_times

    for _ in range(loop_times):
        for _ in range(positions_per_second):
            if positions:
                y, x = positions.pop()
                try:
                    stdscr.addch(y, x, ' ')
                except curses.error:
                    pass
                stdscr.refresh()
        
        time.sleep(in_sec/loop_times)

    stdscr.clear()
    stdscr.refresh()

