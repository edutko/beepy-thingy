import curses

from cashregister import CashRegister, Display, load_catalog


def main(stdscr):
    catalog = load_catalog('./data')
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
    while True:
        try:
            curses.wrapper(main)
        except KeyboardInterrupt:
            break
