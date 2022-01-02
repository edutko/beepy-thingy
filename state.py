from enum import Enum


class State(Enum):
    READY_TO_SCAN = 1
    SCAN = 2
    MANUAL_ENTRY = 3
    READY_TO_PAY = 4
    PAID = 5
    PAID_MULTILINE = 6
