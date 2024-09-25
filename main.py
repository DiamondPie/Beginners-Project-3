### This stuff is a WHOLE MESS and maybe it's not suitable to be in examplers..
### But anyway it's pretty good to watch :)

print("Please wait while we are preparing TUI...")

import curses, time, os
import colors.type, colors.pair
from utils.graphic import flame, clear_screen_randomly
from utils.output import typing, typing_reversely
from utils.get_random_word import getRandomWord, isWordInList

MIN_HEIGHT = 24
MIN_WIDTH = 100
settings = {
    "Play Customised": {
        "Infinite Mode": False,
        "Association Mode": False,
        "Winning Threshold": 3,
        "Word Length": 5
    },
    "Classic Mode": { # Values inside the dict should NOT be changed
        "Infinite Mode": False,
        "Association Mode": False,
        "Winning Threshold": 3,
        "Word Length": 5
    }
}
MENUS = {
    "Classic Mode": {
        "_nodeType": "selective",
        "_childNode": None,
        "_meta": 'Classic mode with basic wordle configs (word length=5)'
    }, 
    "Customise": {
        "_nodeType": "selective",
        "_childNode": {
            "Infinite Mode": {
                "_need": None,
                "_nodeType": "toggle",
                "_childNode": None,
                "_meta": "Play for one time, or until you reach winning threshold"
            },
            "Association Mode": {
                "_need": "Infinite Mode",
                "_nodeType": "toggle",
                "_childNode": None,
                "_meta": "Points awarded are proportionate to how many guesses the user made"
            },
            "Word Length": {
                "_need": None,
                "_nodeType": "number",
                "_min": 3,
                "_max": 10,
                "_childNode": None,
                "_meta": "Sets the length of the word. Use left/right arrow to set value"
            },
            "Winning Threshold": {
                "_need": "Infinite Mode",
                "_nodeType": "number",
                "_min": 3,
                "_max": 1000,
                "_childNode": None,
                "_meta": "Sets the winning threshold. Use left/right arrow to set value"
            },
            "Play Customised": {
                "_nodeType": "selective",
                "_childNode": None,
                "_meta": "Play with the current settings"
            },
        },
        "_meta": 'Config your own game'
    }
}
KEYBOARD = [
    ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
    ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
    ['z', 'x', 'c', 'v', 'b', 'n', 'm']
]

def wait_for_key(stdscr: curses.window, key=None):
    curses.flushinp()
    if key is None:
        while stdscr.getch() == -1: ...
    elif type(key) == str:
        while stdscr.getch() != ord(key): ...
    else:
        while stdscr.getch() != key: ...

def check_window_size(stdscr: curses.window):
    height, width = stdscr.getmaxyx()
    if height >= MIN_HEIGHT and width >= MIN_WIDTH:
        return
    
    while True:
        height, width = stdscr.getmaxyx()

        stdscr.clear()
        stdscr.addstr(1, 10, f"For better performance, please resize the window to at least {MIN_HEIGHT} x {MIN_WIDTH}", curses.color_pair(colors.pair.NORMAL))
        stdscr.addstr(2, 10, f"Current size is {height} x {width}", curses.color_pair(colors.pair.NORMAL))

        flame(stdscr, 0, 8, 5, 75, curses.color_pair(colors.pair.NORMAL), 'round')
        if height < MIN_HEIGHT or width < MIN_WIDTH:
            stdscr.addstr(3, 10, "Window is not large enough", curses.color_pair(colors.pair.WRONG))
        else:
            stdscr.addstr(3, 10, "Press c to continue", curses.color_pair(colors.pair.RIGHT))

        stdscr.refresh()

        c = stdscr.getch()

        if c == ord('c') and (height >= MIN_HEIGHT and width >= MIN_WIDTH):
            break

        time.sleep(0.01)

def show_tip_if_new_player(stdscr: curses.window):
    if not os.path.exists('.REMOVE_ME_TO_SEE_TIPS_AGAIN'):
        typing(stdscr, 1, 10, "A few settings before we start...", curses.color_pair(colors.pair.NORMAL))
        time.sleep(1)
        typing(stdscr, 2, 10, "Please run this in vscode terminal, with default dark theme", curses.color_pair(colors.pair.NORMAL))
        time.sleep(1)
        typing(stdscr, 3, 10, "Also, don't change the size of terminal during running", curses.color_pair(colors.pair.NORMAL))
        time.sleep(1)
        typing(stdscr, 5, 10, "If you're ready, press [       ]", curses.color_pair(colors.pair.NORMAL))
        time.sleep(0.5)
        typing(stdscr, 5, 34, "Any Key", curses.color_pair(colors.pair.KEYS), 0.05)
        time.sleep(0.5)
        typing(stdscr, 5, 43, "to continue", curses.color_pair(colors.pair.NORMAL))
        time.sleep(0.5)

        wait_for_key(stdscr)
        typing(stdscr, 8, 10, "Well, now let's start!", curses.color_pair(colors.pair.NORMAL), 0.01)
        time.sleep(2)

        with open('.REMOVE_ME_TO_SEE_TIPS_AGAIN', 'w') as f:
            f.write('Press .(full stop key) to see answer of current round :)')
        
        clear_screen_randomly(stdscr)
        time.sleep(1)

def main_menu(stdscr: curses.window, menu=None) -> str:
    thismenu = menu or MENUS.copy()
    if menu:
        stdscr.addstr(3, 10, f"Welcome to  ", curses.color_pair(colors.pair.NORMAL))
        stdscr.addstr(f"WORDLE (simplified)", curses.color_pair(colors.pair.WRONGPLACE))
    else:
        typing(stdscr, 3, 10, "Welcome to ", curses.color_pair(colors.pair.NORMAL), 0.1)
        time.sleep(0.5)
        stdscr.addstr(3, 22, "WORDLE (simplified)", curses.color_pair(colors.pair.WRONGPLACE))
        stdscr.refresh()
        time.sleep(1)
        
    menus = list(thismenu.keys())
    for i in range(len(menus)):
        typing_reversely(stdscr, 7+i, 11, menus[i], curses.color_pair(colors.pair.NORMAL), 0.02)
        time.sleep(0.1)

    curses.flushinp()
    stdscr.keypad(True)
    stdscr.nodelay(True)
    option = 0
    while True:
        key = stdscr.getch()

        for i in range(len(menus)):
            stdscr.addstr(7+i, 10, f"  {menus[i]}"+" "*50, curses.color_pair(colors.pair.NORMAL))
        
        if key == curses.KEY_UP and option > 0:
            option -= 1
        elif key == curses.KEY_DOWN and option < len(menus)-1:
            option += 1
        elif key == curses.KEY_ENTER or key in (10, 13):
            if menus[option] in ('Play Customised', 'Classic Mode'):
                return menus[option]
            
            if selecting_submenu['_nodeType'] == 'selective':
                clear_screen_randomly(stdscr, in_sec=1)
                user_choice = main_menu(stdscr, selecting_submenu['_childNode'])
                return user_choice
            elif selecting_submenu['_nodeType'] == 'toggle':
                if not selecting_submenu['_need'] or settings['Play Customised'][selecting_submenu['_need']]:
                    settings['Play Customised'][menus[option]] = not settings['Play Customised'][menus[option]]
        
        selecting_submenu = thismenu[menus[option]]

        if selecting_submenu['_nodeType'] == 'selective':
            stdscr.addstr(7+option, 10, f"> {menus[option]}", curses.color_pair(colors.pair.WRONGPLACE))
        elif selecting_submenu['_nodeType'] == 'toggle':
            if not selecting_submenu['_need'] or settings['Play Customised'][selecting_submenu['_need']]:
                stdscr.addstr(7+option, 10, f"> {menus[option]}: {'ON ' if settings['Play Customised'][menus[option]] else 'OFF'}", curses.color_pair(colors.pair.RIGHT if settings['Play Customised'][menus[option]] else colors.pair.WRONG))
            else:
                stdscr.addstr(7+option, 10, f"> {menus[option]}", curses.color_pair(colors.pair.NOTINCLUDE))
        elif selecting_submenu['_nodeType'] == 'number':
            if '_need' in selecting_submenu and (not selecting_submenu['_need'] or settings['Play Customised'][selecting_submenu['_need']]):
                if key == curses.KEY_RIGHT and settings['Play Customised'][menus[option]] < selecting_submenu['_max']:
                    settings['Play Customised'][menus[option]] += 1
                elif key == curses.KEY_LEFT and settings['Play Customised'][menus[option]] > selecting_submenu['_min']:
                    settings['Play Customised'][menus[option]] -= 1
                stdscr.addstr(7+option, 10, f"> {menus[option]}: {settings['Play Customised'][menus[option]]}", curses.color_pair(colors.pair.WRONGPLACE))
            else:
                stdscr.addstr(7+option, 10, f"> {menus[option]}", curses.color_pair(colors.pair.NOTINCLUDE))

        stdscr.addstr(9+len(menus), 10, " "*80, curses.color_pair(colors.pair.NORMAL))
        if not (meta := selecting_submenu['_meta']) is None:
            stdscr.addstr(9+len(menus), 10, meta, curses.color_pair(colors.pair.EXTRA))

        stdscr.refresh()

def refresh_keyboard(stdscr: curses.window, word_length, update_keys: dict={}, delay=0.1):
    y = 6
    key_initial_x = [20+5*word_length, 22+5*word_length, 25+5*word_length]
    for i, row in enumerate(KEYBOARD):
        x = key_initial_x[i]
        for key in row:
            stdscr.addstr(y, x, '_' if key in update_keys and update_keys[key] == colors.pair.NOTINCLUDE else key, curses.color_pair(update_keys[key] if key in update_keys else colors.pair.NORMAL))
            if delay: 
                stdscr.refresh()
                time.sleep(delay)
            x += 4
        y += 2

    stdscr.refresh()

def check_settings():
    user_settings = settings['Play Customised']
    if user_settings['Infinite Mode'] and user_settings['Increasing Mode']:
        user_settings['Word Length'] = 3
    else:
        user_settings['Association Mode'] = False
        user_settings['Increasing Mode'] = False

def main_game(stdscr: curses.window, user_choice, user_score=0):
    user_settings = settings[user_choice]
    word_length = user_settings['Word Length']

    input_x = list(range(12, 13+5*(word_length-1), 5))
    input_y = list(range(1, 17, 3))

    # Construct input area
    for y in input_y:
        for x in input_x:
            flame(stdscr, y, x-2, 3, 5, curses.color_pair(colors.pair.NORMAL), 'round')
        stdscr.refresh()
        time.sleep(0.2)
    refresh_keyboard(stdscr, word_length, delay=0.05)
    if user_settings['Infinite Mode']:
        typing(stdscr, 13, 25+5*word_length, "Points you have earned: ", curses.color_pair(colors.pair.NORMAL))
        time.sleep(0.1)
        typing(stdscr, None, None, f"{user_score}", curses.color_pair(colors.pair.KEYS), 0.1)
        typing(stdscr, None, None, f"/{user_settings['Winning Threshold']}", curses.color_pair(colors.pair.NORMAL), 0.1)
        time.sleep(0.1)

    user_round = 0
    answer = getRandomWord(word_length)
    is_won = False
    keys = {}
    while True: # one game of each word
        if user_round >= 6:
            break

        word = ""
        stdscr.keypad(True)
        curses.flushinp()
        while True:
            key = stdscr.getch()
            if key == curses.KEY_ENTER or key in (10, 13):
                if len(word) < word_length:
                    for _ in range(3):
                        stdscr.addstr(20, 10, "Not enough letters", curses.color_pair(colors.pair.WRONG))
                        stdscr.refresh()
                        time.sleep(0.2)
                        stdscr.addstr(20, 10, " "*30, curses.color_pair(colors.pair.NORMAL))
                        stdscr.refresh()
                        time.sleep(0.1)
                    curses.flushinp()
                    continue
                elif not isWordInList(word):
                    for _ in range(3):
                        stdscr.addstr(20, 10, "I'm sorry, but this is not a word!", curses.color_pair(colors.pair.WRONG))
                        stdscr.refresh()
                        time.sleep(0.2)
                        stdscr.addstr(20, 10, " "*50, curses.color_pair(colors.pair.NORMAL))
                        stdscr.refresh()
                        time.sleep(0.1)
                    curses.flushinp()
                    continue
                else:
                    break
            elif key == ord('.'):
                stdscr.addstr(20, 10, f"DEBUG: Word is {answer}", curses.color_pair(colors.pair.EXTRA))
                stdscr.refresh()
                time.sleep(1)
                stdscr.addstr(20, 10, " "*30, curses.color_pair(colors.pair.NORMAL))
                stdscr.refresh()
                curses.flushinp()
                continue
            elif word and (key == curses.KEY_BACKSPACE or key in (8, 127)):
                word = word[:-1]
            elif len(word) < word_length and (97 <= key <= 122):
                word += chr(key)

            for x, c in zip(input_x, word+' '*(word_length-len(word))):
                flame(stdscr, input_y[user_round], x-2, 3, 5, curses.color_pair(colors.pair.NORMAL), 'round')
                stdscr.addstr(input_y[user_round]+1, x, c, curses.color_pair(colors.pair.NORMAL))
            if len(word) < word_length: flame(stdscr, input_y[user_round], input_x[len(word)]-2, 3, 5, curses.color_pair(colors.pair.EXTRA), 'round')
            # stdscr.addstr(input_y[user_round]+1, x, word[-1], curses.color_pair(colors.pair.EXTRA))
            stdscr.refresh()
        
        time.sleep(0.5)
        for i in range(word_length):
            letter = word[i]
            if answer[i] == letter:
                flame(stdscr, input_y[user_round], input_x[i]-2, 3, 5, curses.color_pair(colors.pair.RIGHT), 'round')
                stdscr.addstr(input_y[user_round]+1, input_x[i], letter, curses.color_pair(colors.pair.RIGHT))
                keys[letter] = colors.pair.RIGHT
            elif letter in answer:
                flame(stdscr, input_y[user_round], input_x[i]-2, 3, 5, curses.color_pair(colors.pair.WRONGPLACE), 'round')
                stdscr.addstr(input_y[user_round]+1, input_x[i], letter, curses.color_pair(colors.pair.WRONGPLACE))
                if letter not in keys or keys[letter] < colors.pair.WRONGPLACE: keys[letter] = colors.pair.WRONGPLACE
            else:
                flame(stdscr, input_y[user_round], input_x[i]-2, 3, 5, curses.color_pair(colors.pair.NOTINCLUDE), 'round')
                stdscr.addstr(input_y[user_round]+1, input_x[i], letter, curses.color_pair(colors.pair.NOTINCLUDE))
                keys[letter] = colors.pair.NOTINCLUDE
            stdscr.refresh()
            time.sleep(0.2)
        
        refresh_keyboard(stdscr, word_length, keys, delay=0)

        user_round += 1
        if answer == word:
            is_won = True
            break
    
    if is_won:
        if user_settings['Infinite Mode'] and user_settings['Association Mode']:
            earned_points = 7 - user_round
            typing(stdscr, 20, 10, f"Congrats! You guessed the word with {earned_points} points!", curses.color_pair(colors.pair.RIGHT))
            time.sleep(1)
            for i in range(user_score, user_score+earned_points):
                stdscr.addstr(13, 25+5*word_length, f"Points you have earned: ", curses.color_pair(colors.pair.NORMAL))
                stdscr.addstr(f"{i+1}", curses.color_pair(colors.pair.KEYS))
                stdscr.addstr(f"/{user_settings['Winning Threshold']}", curses.color_pair(colors.pair.NORMAL))
                stdscr.refresh()
                time.sleep(0.1)
            user_score += earned_points
        else:
            user_score += 1
            typing(stdscr, 20, 10, f"Congrats! You guessed the word!", curses.color_pair(colors.pair.RIGHT))
            time.sleep(1)
            if user_settings['Infinite Mode']:
                stdscr.addstr(13, 25+5*word_length, f"Points you have earned: ", curses.color_pair(colors.pair.NORMAL))
                stdscr.addstr(f"{user_score}", curses.color_pair(colors.pair.KEYS))
                stdscr.addstr(f"/{user_settings['Winning Threshold']}", curses.color_pair(colors.pair.NORMAL))
                stdscr.refresh()
    else:
        typing(stdscr, 20, 10, f"Sorry, you lost. The word was ", curses.color_pair(colors.pair.NORMAL))
        typing(stdscr, None, None, answer, curses.color_pair(colors.pair.KEYS), 0.1)
    
    time.sleep(1)
    typing(stdscr, 21, 10, "Press [       ]", curses.color_pair(colors.pair.NORMAL))
    time.sleep(0.1)
    typing(stdscr, 21, 17, "Any Key", curses.color_pair(colors.pair.KEYS), 0.05)
    time.sleep(0.1)
    typing(stdscr, 21, 26, "to continue", curses.color_pair(colors.pair.NORMAL))

    curses.flushinp()
    wait_for_key(stdscr)
    clear_screen_randomly(stdscr)

    if user_settings['Infinite Mode'] and user_score < user_settings['Winning Threshold']: 
        main_game(stdscr, user_choice, user_score)

def main(stdscr: curses.window):
    os.system('cls')
    curses.curs_set(0)
    stdscr.nodelay(True) 
    stdscr.timeout(100)
    curses.use_default_colors()

    if not curses.can_change_color():
        return

    curses.init_color(colors.type.PLAIN, 700, 700, 700)
    curses.init_color(colors.type.BACKGROUND, 94, 94, 94)
    curses.init_color(colors.type.KEYS, 100, 500, 100)
    curses.init_color(colors.type.RIGHT, 600, 1000, 600)
    curses.init_color(colors.type.WRONG, 1000, 600, 600)
    curses.init_color(colors.type.EXTRA, 600, 700, 1000)
    curses.init_color(colors.type.WRONGPLACE, 900, 700, 400)
    curses.init_color(colors.type.NOTINCLUDE, 300, 300, 300)
    curses.init_pair(colors.pair.NORMAL, colors.type.PLAIN, colors.type.BACKGROUND)
    curses.init_pair(colors.pair.KEYS, colors.type.KEYS, colors.type.BACKGROUND)
    curses.init_pair(colors.pair.RIGHT, colors.type.RIGHT, colors.type.BACKGROUND)
    curses.init_pair(colors.pair.WRONG, colors.type.WRONG, colors.type.BACKGROUND)
    curses.init_pair(colors.pair.EXTRA, colors.type.EXTRA, colors.type.BACKGROUND)
    curses.init_pair(colors.pair.WRONGPLACE, colors.type.WRONGPLACE, colors.type.BACKGROUND)
    curses.init_pair(colors.pair.NOTINCLUDE, colors.type.NOTINCLUDE, colors.type.BACKGROUND)
    
    stdscr.bkgd(' ', curses.color_pair(colors.pair.NORMAL))
    check_window_size(stdscr)

    stdscr.clear()
    show_tip_if_new_player(stdscr)
    user_choice = main_menu(stdscr)
    # check_settings()
    clear_screen_randomly(stdscr)
    main_game(stdscr, user_choice)
    time.sleep(1)
    typing(stdscr, 3, 12, "Thanks for playing! :P", curses.color_pair(colors.pair.EXTRA), 0.05)
    time.sleep(1)
    typing(stdscr, 4, 12, "btw I don't think this can be on exampler since it's too complicated ( ╯□╰ )", curses.color_pair(colors.pair.NORMAL))
    time.sleep(1)
    for i in range(3):
        stdscr.addstr(6, 12, f"Returning to terminal prompt in {3-i} seconds...", curses.color_pair(colors.pair.NORMAL))
        stdscr.refresh()
        time.sleep(1)

if __name__ == '__main__':
    curses.wrapper(main)
