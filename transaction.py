class Transaction(object):
    def __init__(self, raw: str = '', price: float = None, label: str = None):
        self.raw = raw
        self.price = price
        self.label = label
