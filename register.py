import math
import random
from typing import List, Dict

from display import Display
from items import Item
from state import State
from transaction import Transaction


class CashRegister(object):
    def __init__(self, display: Display, items: Dict[str, Item] = None):
        self.display: Display = display
        self.item_db: Dict[str, Item] = {} if items is None else items
        self.state: State = State.READY_TO_SCAN
        self.transactions: List[Transaction] = []
        self.curr_txn: Transaction = Transaction()
        self.rng = random.Random()

        display.change_state(self.state)

    def change_state(self, s: State):
        self.state = s
        self.display.change_state(s)

    def commit_current_transaction(self):
        if self.curr_txn.raw.lower() in self.item_db:
            self.curr_txn.label = self.item_db[self.curr_txn.raw.lower()].label
            self.curr_txn.price = self.item_db[self.curr_txn.raw.lower()].price
        if self.curr_txn.label is None:
            self.curr_txn.label = self.curr_txn.raw
        if self.curr_txn.price is None:
            self.curr_txn.price = self.random_price()

        self.transactions.append(self.curr_txn)
        self.display.add_transaction(self.curr_txn)
        self.curr_txn = Transaction()

    def clear_transactions(self):
        self.curr_txn = Transaction()
        self.transactions = []

    def handle_input(self, c, multiline: bool = False):
        if self.state == State.READY_TO_SCAN:
            self.curr_txn.raw += c
            self.change_state(State.SCAN)

        elif self.state == State.SCAN or self.state == State.MANUAL_ENTRY:
            if c == '\n':
                self.commit_current_transaction()
            elif c == '*':
                self.display.set_total(self.get_total())
                self.change_state(State.READY_TO_PAY)
            else:
                self.curr_txn.raw += c

        elif self.state == State.READY_TO_PAY:
            if c == '\n':
                if multiline:
                    self.change_state(State.PAID_MULTILINE)
                else:
                    self.change_state(State.PAID)

        elif self.state == State.PAID_MULTILINE:
            if c == '\n':
                self.change_state(State.PAID)

        elif self.state == State.PAID:
            self.clear_transactions()
            self.curr_txn.raw += c
            self.change_state(State.SCAN)

        else:
            self.transactions = []
            self.curr_txn = Transaction()
            self.change_state(State.READY_TO_SCAN)

    def random_price(self):
        return math.floor(self.rng.random() * 20) + 0.99

    def get_transactions(self):
        return self.transactions

    def get_total(self):
        return sum([t.price for t in self.transactions])
