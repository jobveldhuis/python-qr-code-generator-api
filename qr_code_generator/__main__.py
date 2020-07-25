#!/usr/bin/env python3
from wrapper import QrGenerator
import argparse


def main():
    """Main entry function, parses arguments, creates an instance of the wrapper and requests QR codes."""
    parser = create_parser()
    args = parser.parse_args()

    # When an API token is explicitly specified, set it. Else, initialize without token.
    if args.token:
        api = QrGenerator(args.token)
    else:
        api = QrGenerator()

    # If a configuration file to load from has been found, load it to the app config
    if args.config:
        api.config.load(args.config)

    # If output filename is specified, set filename in app
    if args.output:
        api.output_filename = args.output

    # If verbose flag is added, overwrite configuration to set VERBOSE to True
    if args.verbose:
        api.config['VERBOSE'] = True

    # If bulk requests are made, we should enumerate them and give them specific names
    if args.bulk:
        if api.output_filename:
            name = api.output_filename
            for i in range(1, args.bulk + 1):
                api.output_filename = f'{name}-{i}'
                api.request()
        else:
            for i in range(1, args.bulk + 1):
                api.request()
    else:
        api.request()


def create_parser():
    """
    Create argument parser for command line interface

    Returns
    -------
    parser : ArgumentParser
        The parser with arguments, that will parse the console command
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--token', help='access token for the API', type=str, metavar='')
    parser.add_argument('-c', '--config', help='relative path to config.ini file to load settings from', type=str,
                        metavar='')
    parser.add_argument('-o', '--output', help='output filename without extension', type=str, metavar='')
    parser.add_argument('-b', '--bulk', help='amount of files to generate', type=int, metavar='')
    parser.add_argument('-v', '--verbose', help='whether or not debug logs should show', action='store_true')
    return parser


if __name__ == "__main__":
    """Main entry point, calls main entry function"""
    main()
