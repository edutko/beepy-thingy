import argparse
import logging

from cashregister import load_catalog

parser = argparse.ArgumentParser()
parser.add_argument("--load-only", help="populate the sqlite database and exit", action="store_true")

args = parser.parse_args()
if not args.load_only:
    import curses
    from cashregister import CashRegister, Display


def main(stdscr, catalog):
    display = Display(stdscr)
    register = CashRegister(display, catalog)
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
    args = parser.parse_args()
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', datefmt='%H:%M:%S', level=logging.INFO)
    itemdb = load_catalog('./data')
    try:
        if not args.load_only:
            while True:
                try:
                    curses.wrapper(main, itemdb)
                except KeyboardInterrupt:
                    break
    finally:
        itemdb.close()
