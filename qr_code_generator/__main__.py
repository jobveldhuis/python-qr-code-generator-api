#!/usr/bin/env python3
from qr_code_generator import QrGenerator
import sys


def main(**kwargs):
    if 'access-token' in kwargs:
        token = kwargs['access-token']
        kwargs.pop('access-token', None)
        api = QrGenerator(token, **kwargs)
    else:
        api = QrGenerator(**kwargs)
    print(api.get_option('API_URI', 'config'))


if __name__ == "__main__":
    if len(sys.argv) != 1:
        args = {}
        for arg in sys.argv[1:]:
            key = arg.split('=')[0]
            value = ''.join(arg.split('=')[1:])
            if key in args:
                raise ValueError('Double defined key in calling arguments')
            if not value:
                raise ValueError('Missing value for at least one argument')
            args[key] = value
        main(**args)
    else:
        main()
