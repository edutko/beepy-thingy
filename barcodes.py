import os
from typing import List

import barcode

from items import fruits, vegetables


def img_filename(i: int):
    return 'barcode-{}'.format(i)


def generate_barcodes(name: str, items: List[str], cols: int, rows: int, base_dir: str = '.'):
    index_dir = os.path.join(base_dir, name)
    image_dir = os.path.join(index_dir, 'images')

    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    with open(os.path.join(index_dir, 'index.html'), 'w') as f:
        f.write('<html>\n<body>\n<table style="width: 100%; height: 100%; border: 0px;">\n')
        for r in range(0, rows):
            f.write('  <tr>\n')
            for c in range(0, cols):
                f.write('    <td style="text-align: center; vertical-align: center;">'
                        '<img src="{}/{}.svg"/></td>\n'.format(os.path.basename(image_dir), img_filename(r * cols + c)))
            f.write('  </tr>\n')
        f.write('</table>\n</body>\n</html>\n')

    for i in range(0, rows * cols):
        b = barcode.get('code128', items[i])
        b.save(os.path.join(image_dir, img_filename(i)))


def main():
    generate_barcodes('fruit', [i.label for i in fruits], rows=10, cols=3)
    generate_barcodes('vegetables', [i.label for i in vegetables], rows=10, cols=3)
    generate_barcodes('numbers', ['{:08}'.format(n) for n in range(0, 50)], rows=10, cols=5)


if __name__ == '__main__':
    main()
