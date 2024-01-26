#!/usr/bin/env python3
import pyfiglet
import argparse


def ascii_art(name, font):
    ascii_name = pyfiglet.figlet_format(name, font=font)
    return ascii_name


def main():
    parser = argparse.ArgumentParser(
        description="Takes a string, returns an ascii_font",
        formatter_class=argparse.HelpFormatter
    )
    parser.add_argument(
        '-s', '--string',
        type=str,
        help='Input String'
    )
    parser.add_argument(
        '-f', '--font',
        type=str,
        default='slant',
        help='PyFiglet ascii fonts'
    )
    parser.add_argument(
        '-l', '--list_fonts',
        action='store_true',
        help='List fonts'
    )

    args = parser.parse_args()

    if args.list_fonts:
        print(pyfiglet.FigletFont.getFonts())
    else:
        print(ascii_art(args.string, args.font))


if __name__ == "__main__":
    main()
