#!/usr/bin/env python3
class Config(dict):
    """
    Configuration class, behaves just like a dict
    """
    def __init__(self, *args, **kwargs):
        super(Config, self).__init__(*args, **kwargs)

        # Basic configuration values
        self['API_URI'] = 'https://api.qr-code-generator.com/v1/create?'
        self['FORCE_OVERWRITE'] = False
        self['REQUIRED_PARAMETERS'] = [
            'access-token',
            'qr_code_text'
        ]
        self['OUT_FOLDER'] = 'out'
        self['OUTPUT_FOLDER'] = 'test'

    def get(self, key):
        try:
            return self[key]
        except KeyError:
            return None

    def set(self, key, value):
        if key not in self:
            raise KeyError
        else:
            self[key] = value
