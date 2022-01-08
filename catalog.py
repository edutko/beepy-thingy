import os.path
from typing import Dict, List, Optional, Set, Iterable

from prices import random_price


class Item(object):
    def __init__(self, code: str = None, price: float = None, label: str = None, dataset: str = None):
        self.code = code
        self.price = price
        self.label = label if label is not None else code
        self.dataset = dataset


class Catalog(object):
    def __init__(self, data_dir: str = None):
        self._items: Dict[str, Item] = {}
        self._datasets: Set[str] = set()
        self._data_dir = data_dir

    def load_dataset(self, dataset_file: str):
        dataset = os.path.splitext(dataset_file)[0]
        data_file = os.path.join(self._data_dir, dataset_file)
        with open(data_file, 'r') as f:
            n = 0
            for line in f:
                n += 1
                cols = line.rstrip().split('\t')
                if len(cols) < 2 or cols[0].strip() == '':
                    print('WARNING: invalid record in {}, line {}: "{}"'.format(data_file, n, line))
                    continue
                self._add_item(Item(
                    code=cols[0].strip(),
                    label=cols[1].strip(),
                    price=float(cols[2].strip()) if len(cols) > 2 else None,
                    dataset=dataset
                ))

    def load(self):
        for f in filter(lambda x: not x.startswith('.') and x.endswith('.tsv'), os.listdir(self._data_dir)):
            if os.path.isfile(os.path.join(self._data_dir, f)):
                self.load_dataset(f)

    def save_dataset(self, dataset: str):
        if not os.path.exists(self._data_dir):
            os.makedirs(self._data_dir)
        file_path = os.path.join(self._data_dir, dataset + '.tsv')
        if not os.path.exists(file_path) or os.access(file_path, os.W_OK):
            with open(file_path, 'w') as f:
                for item in self.get_items_in_dataset(dataset):
                    f.write('{}\t{}\t{:.2f}\n'.format(item.code, item.label, item.price))

    def save(self):
        for dataset in self._datasets:
            self.save_dataset(dataset)

    def _add_item(self, item: Item):
        if item.label is None:
            item.label = item.code
        if item.price is None:
            item.price = random_price()
        if item.dataset is None:
            item.dataset = 'custom'
        self._items[item.code] = item
        self._datasets.add(item.dataset)

    def add_item(self, item: Item):
        self._add_item(item)
        self.save_dataset('custom')

    def get_items_in_dataset(self, dataset: str) -> Iterable[Item]:
        if dataset not in self._datasets:
            return []
        return filter(lambda itm: itm.dataset == dataset, self._items.values())

    def lookup_item_by_code(self, code: str) -> Optional[Item]:
        return self._items.get(code)


def load_catalog(data_dir: str) -> Catalog:
    catalog = Catalog(data_dir=data_dir)
    catalog.load()
    return catalog
