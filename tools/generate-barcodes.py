import os
from typing import Iterable, List

import barcode

from util import read_tsv_file


def generate_barcodes(name: str, items: Iterable[List[str]], cols: int = 4, base_dir: str = 'barcodes'):
    index_dir = os.path.join(base_dir, name)
    image_dir = os.path.join(index_dir, 'images')

    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    with open(os.path.join(index_dir, 'index.html'), 'w') as f:
        f.write('<html>\n<body>\n<table style="width: 100%; height: 100%; border: 0px;">\n')
        count = 0
        for i in items:
            if count % cols == 0:
                f.write('  <tr>\n')

            b = barcode.get('code128', i[0])
            img_filename = b.save(os.path.join(image_dir, 'barcode-{}'.format(count)))
            f.write('    <td style="text-align: center; vertical-align: center;"><img src="{}/{}"/></td>\n'
                    .format(os.path.basename(image_dir), os.path.basename(img_filename)))

            if count % cols == cols - 1:
                f.write('  </tr>\n')
            count += 1

        f.write('</table>\n</body>\n</html>\n')


def main():
    generate_barcodes('fruits', read_tsv_file('sample-data/fruits.tsv', select_columns=[0]), cols=3)
    generate_barcodes('vegetables', read_tsv_file('sample-data/vegetables.tsv', select_columns=[0]), cols=3)
    generate_barcodes('numbers', [['{:08}'.format(n)] for n in range(0, 50)], cols=5)


if __name__ == '__main__':
    main()
