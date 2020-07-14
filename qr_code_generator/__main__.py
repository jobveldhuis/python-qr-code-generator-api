#!/usr/bin/env python3
from wrapper import QrGenerator
import sys
import argparse


def main():
    """Main entry point"""
    parser = create_parser()
    args = parser.parse_args()
    if args.token:
        api = QrGenerator(args.token)
    else:
        api = QrGenerator()


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--token', help='access token for the API', type=str, metavar='')
    parser.add_argument('-c', '--config', help='config.ini file to load settings from', type=str, metavar='')
    parser.add_argument('-o', '--output', help='output filename without extension', type=str, metavar='')
    return parser


if __name__ == "__main__":
    main()
