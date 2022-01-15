from typing import List


def read_tsv_file(tsv_file: str, select_columns: List[int] = None, nonblank_columns: List[int] = None):
    nonblank_columns = [] if nonblank_columns is None else nonblank_columns
    with open(tsv_file, 'r', encoding='utf-8') as f:
        n = 0
        for line in f:
            n += 1
            cols = line.rstrip().split('\t')
            if not is_row_valid(cols, nonblank_columns):
                print('WARNING: invalid record in {}, line {}: "{}"'.format(tsv_file, n, line.rstrip()))
                continue
            if select_columns is None:
                yield cols
            else:
                yield [cols[i] if i < len(cols) else None for i in select_columns]


def is_row_valid(cols, nonblank_columns: List[int]):
    for c in nonblank_columns:
        if c >= len(cols) or cols[c].strip() == '':
            return False
    return True
