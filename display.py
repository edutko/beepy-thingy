import curses
from enum import Enum

from state import State
from transaction import Transaction


class Color(Enum):
    WHITE_ON_BLACK = 0
    RED_ON_BLACK = 1
    GREEN_ON_BLACK = 2
    YELLOW_ON_BLACK = 3
    BLUE_ON_BLACK = 4
    MAGENTA_ON_BLACK = 5
    CYAN_ON_BLACK = 6


class Display(object):
    def __init__(self, stdscr):
        self._total: float = 0.0
        self.stdscr = stdscr
        self.stdscr.scrollok(True)
        curses.curs_set(0)
        curses.init_pair(Color.RED_ON_BLACK.value, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(Color.GREEN_ON_BLACK.value, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(Color.YELLOW_ON_BLACK.value, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(Color.BLUE_ON_BLACK.value, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(Color.MAGENTA_ON_BLACK.value, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(Color.CYAN_ON_BLACK.value, curses.COLOR_CYAN, curses.COLOR_BLACK)

    def add_transaction(self, t: Transaction):
        (_, w) = self.stdscr.getmaxyx()
        label = t.label[:w - 15] if len(t.label) > w - 15 else t.label
        self.stdscr.addstr('{}{:>7.2f}\n'.format(label.ljust(w - 10), t.price))
        self.stdscr.refresh()

    def set_total(self, total: float):
        self._total = total

    def ready_to_scan(self):
        self.stdscr.clear()
        self._addstr_centered('Scan or enter an item to begin.', Color.CYAN_ON_BLACK)
        self.stdscr.refresh()

    def scan(self):
        self.stdscr.clear()
        self.stdscr.refresh()

    def ready_to_pay(self):
        self.stdscr.clear()
        self._addstr_centered('Total: ${:.2f}\nSwipe or insert payment card.'.format(self._total), Color.YELLOW_ON_BLACK)
        self.stdscr.refresh()

    def paid(self):
        self.stdscr.clear()
        self._addstr_centered('Thank you. Have a nice day!', Color.GREEN_ON_BLACK)
        self.stdscr.refresh()
        curses.napms(3000)
        self.ready_to_scan()

    def change_state(self, state: State):
        if state == State.READY_TO_SCAN:
            self.ready_to_scan()
        elif state == State.SCAN:
            self.scan()
        elif state == State.READY_TO_PAY:
            self.ready_to_pay()
        elif state == State.PAID:
            self.paid()

    def _addstr_centered(self, s: str, color: Color = Color.WHITE_ON_BLACK):
        lines = s.split('\n')
        (h, w) = self.stdscr.getmaxyx()
        r0 = h // 2
        r0 -= (len(lines) // 2)
        for i in range(0, len(lines)):
            c = w // 2
            c -= (len(lines[i]) // 2)
            self.stdscr.addstr(r0 + i, c, lines[i], curses.color_pair(color.value))
