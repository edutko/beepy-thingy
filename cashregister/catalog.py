import logging
import os.path
import sqlite3
from functools import lru_cache
from typing import Optional

from util import read_tsv_file
from .prices import random_price


class Item(object):
    def __init__(self, code: str = None, price: float = None, label: str = None):
        self.code = code
        self.price = price
        self.label = label if label is not None else code


class Catalog(object):
    def __init__(self, data_dir: str = None):
        self._data_dir = data_dir
        self._db: Optional[sqlite3.Connection] = None
        self.BATCH_SIZE = 10000

    def load(self):
        if self._db is not None:
            self.close()
        self._db = sqlite3.connect(os.path.join(self._data_dir, 'catalog.db'))
        self._db.row_factory = sqlite3.Row
        with self._db:
            self._db.execute('CREATE TABLE IF NOT EXISTS items (code TEXT NOT NULL, price REAL, label TEXT)')
            self._db.execute('CREATE TABLE IF NOT EXISTS datasets (path TEXT NOT NULL, mtime INTEGER NOT NULL)')
            self._db.execute('CREATE INDEX IF NOT EXISTS datasets_by_path ON datasets (path)')

        for f in filter(lambda x: not x.startswith('.') and x.endswith('.tsv'), os.listdir(self._data_dir)):
            if f == 'custom.tsv':
                continue
            if os.path.isfile(os.path.join(self._data_dir, f)):
                self._load_dataset(f)

        # Load custom data last so that custom values override stock values
        f = 'custom.tsv'
        if os.path.isfile(os.path.join(self._data_dir, f)):
            self._load_dataset(f)

        logging.info('Indexing items...')
        with self._db:
            self._db.execute('CREATE INDEX IF NOT EXISTS item_by_code ON items (code)')

    def close(self):
        if self._db is not None:
            self._db.close()
            self._db = None

    @lru_cache(maxsize=1024)
    def lookup_item_by_code(self, code: str) -> Optional[Item]:
        with self._db:
            cur = self._db.cursor()
            cur.execute('SELECT code, label, price FROM items WHERE code = ?', (code,))
            row = cur.fetchone()
            if row is not None:
                return self._new_item(Item(
                    code=row['code'],
                    price=row['price'],
                    label=row['label'],
                ))
            return None

    def add_custom_item(self, item: Item):
        itm = self._new_item(item)
        self._append_item_to_dataset('custom', itm)
        self._db.execute('INSERT OR REPLACE INTO items (code, price, label) VALUES (?, ?, ?)',
                         (itm.code, itm.price, itm.label))

    def _load_dataset(self, dataset_file: str, force: bool = False):
        data_file = os.path.abspath(os.path.normpath(os.path.join(self._data_dir, dataset_file)))
        mtime = int(os.path.getmtime(data_file))
        with self._db:
            cur = self._db.cursor()
            if not force:
                cur.execute('SELECT mtime FROM datasets WHERE path = ?', (dataset_file,))
                row = cur.fetchone()
                if row is not None and mtime == row['mtime']:
                    logging.info('Skipping unmodified dataset "{}".'.format(dataset_file, mtime))
                    return
            logging.info('Loading dataset "{}"...'.format(dataset_file, mtime))
            count = 0
            for (code, price, label) in read_tsv_file(data_file, select_columns=[0, 1, 2], nonblank_columns=[0]):
                price = None if price.strip() == '' else price
                cur.execute('INSERT OR REPLACE INTO items (code, price, label) VALUES (?, ?, ?)', (code, price, label))
                count += 1
                if count % self.BATCH_SIZE == 0:
                    self._db.commit()
            cur.execute('INSERT OR REPLACE INTO datasets (path, mtime) VALUES (?, ?)', (dataset_file, mtime))
            cur.close()

    def _append_item_to_dataset(self, dataset: str, item: Item):
        if not os.path.exists(self._data_dir):
            os.makedirs(self._data_dir)
        file_path = os.path.join(self._data_dir, dataset + '.tsv')
        if not os.path.exists(file_path) or os.access(file_path, os.W_OK):
            with open(file_path, 'a') as f:
                f.write('{}\t{:.2f}\t{}\n'.format(item.code, item.price, item.label))

    @staticmethod
    def _new_item(item: Item):
        if item.price is None:
            item.price = random_price()
        if item.label is None:
            item.label = item.code
        return item


def load_catalog(data_dir: str) -> Catalog:
    catalog = Catalog(data_dir=data_dir)
    catalog.load()
    return catalog
