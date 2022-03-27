# toy-cash-register

Curses-based cash register for kids

## Hardware

The cash register should run on any general-purpose computer. It is designed for small, inexpensive systems like a
Raspberry Pi. A Raspberry Pi 2 or above should work fine, but very large catalogs will take a long time to load the
first time the cash register runs.

Any display will work, but it is optimized for small displays and low resolutions.

It's possible to operate the cash register using a regular keyboard, but peripherals like a barcode scanner, a number
pad, and a card reader make it much more fun.

My setup uses the following hardware:

* [Raspberry Pi 3](https://www.raspberrypi.com/products/)
* [7" TFT HDMI display](https://smile.amazon.com/SunFounder-Inch-Screen-Monitor-HDMI/dp/B012ZRYDYY/)
* [USB barcode scanner](https://smile.amazon.com/gp/product/B08TWX74T4/)
* [USB numeric keypad](https://smile.amazon.com/gp/product/B01M4NH7F9/)
* [USB magnetic card reader](https://smile.amazon.com/gp/product/B0183PUZMQ/)

I included links to specific items for clarity, but please consider purchasing from local businesses when possible.

## Prerequisites

### Raspberry Pi

If you're using a Raspberry Pi, a minimal installation of Raspbian will work
(no graphical desktop required). For optimal viewing on a small screen like the one listed above, set the resolution of
the console to 640x480 (CEA mode 1) or 720x576 (CEA mode 17):

**Option 1**

1. `sudo raspi-config`
2. Select `7 Advanced Options`
3. Select `A5 Resolution`
4. Choose `CEA Mode 1 640x480 60Hz 4:3` or `CEA Mode 17 720x576 50Hz 4:3`.
5. Save the settings and reboot.

**Option 2**

1. `nano /boot/config.txt`
2. Change `#hdmi_group=` to `hdmi_group=1` (640x480 60Hz) or `hdmi_group=17` (720x576 50Hz).
3. Save the file and reboot.

You may also need to install some software on the Pi:

`sudo apt install git python3`

### Windows

If you're using Windows, you'll need to install Windows Subsytem for Linux
(WSL) or Cygwin. You'll need Python 3, which may already be installed.

### MacOS

I haven't tested on MacOS, but it should work. If you're using a MacBook, you'll probably
need [a bunch of dongles](https://www.youtube.com/watch?v=-XSC_UG5_kU)
to connect all the peripherals.

## Installation

`git clone https://github.com/edutko/toy-cash-register.git`

## Configuration

No configuration is required. By default, the cash register will display the value of a scanned barcode and generate a
random price. This is probably sufficient for young kids who just like the fun of "beeping" things with the scanner.

However, the cash register can also read data from tab-delimited (TSV) files containing human-friendly labels and (
optional) prices.

### Quick Start

Create a `data` folder under `toy-cash-register`. The first time you run the cash register, it will read every `.tsv`
file in the `data` folder and use that data to display human-friendly labels and consistent prices (rather than the
default behavior of displaying the barcode value and generating a random price.)

The [sample-data](./sample-data) folder contains some pre-created `.tsv` files you can use. `wic-nc.tsv` contains real
UPC codes that can be found on a variety of groceries. `fruts.tsv` and `vegetables.tsv` are meant to be used with
generated barcodes that you print (and maybe tape to plastic toy food).

[generate-barcodes.py](./tools/generate-barcodes.py) will create three folders, each with an `index.html` that you can
open in a browser and print. (You'll need to copy the
`.tsv` files to the `data` directory to get consistent prices, but since the barcodes are just encodings of the labels,
everything else will work even if you forget to copy the files.)

If you want to use the tools, you may want to use virtualenv and install the dependencies into the virtualenv
environment.

```
pip3 install virtualenv
python3 -m venv venv
. venv/bin/activate
pip -r tools/requirements.txt
python3 tools/generate-barcodes.py
```

### Advanced

The cash register will read each `.tsv` file in the `data` folder when it starts. (Technically, it only reads files that
are new or have changed since it last read them.) This allows you to easily add labels and prices for any barcodes your
kid wants to scan.

If you live in the United States, your state may publish its WIC database
(including UPC codes) online. I found one for North Carolina and converted it to the TSV format expected by the cash
register. (See
[data/wic-nc.tsv](./data/wic-nc.tsv).) This is a lot of fun for the kids because they can scan things like cereal boxes
and see the real name on the display.

Since the cash register uses a sqlite database to index its catalog of items, you can load very large datasets and still
get good performance. The cash register will take a while to load everything the first time, but unless you modify the
TSV files, it will start quickly every subsequent time.

## Use

The cash register itself has no external dependencies, so you can run it as follows:

`python3 main.py`

1. Scan items with the scanner (or type numbers on the keypad and press `Enter`).
2. When ready to "check out," press `*`.
3. Slide a card through the card reader (or type some numbers and press `Enter`).
4. Repeat until bored.

You can also add items interactively without the need to edit TSV files:

1. Press `/`.
2. Follow the prompts to scan/enter the barcode, label, and price. The new item will be saved permanently.
