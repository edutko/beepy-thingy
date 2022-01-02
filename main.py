import curses
from typing import Dict

import items
from register import CashRegister, Display


def build_item_db():
    item_db: Dict[str, items.Item] = {}
    for item_list in items.all_items:
        for item in item_list:
            item_db[item.label.lower()] = item
    return item_db


def main(stdscr):
    display = Display(stdscr)
    register = CashRegister(display, build_item_db())
    while True:
        k = stdscr.getkey()
        multiline = False
        if k == '\n':
            curses.napms(50)
            stdscr.nodelay(True)
            c = stdscr.getch()
            if c != -1:
                multiline = True
                curses.ungetch(c)
            stdscr.nodelay(False)
        register.handle_input(k, multiline)


if __name__ == '__main__':
    while True:
        try:
            curses.wrapper(main)
        except KeyboardInterrupt:
            break
