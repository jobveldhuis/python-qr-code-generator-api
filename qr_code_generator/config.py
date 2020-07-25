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
        self['OUTPUT_FOLDER'] = 'output'
        self['VERBOSE'] = False

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

    def load(self, file):
        extension = file.split('.')[-1]
        if not extension == 'ini':
            raise ValueError('Selected file is not a .ini file')
        with open(file, "r") as f:
            content = f.readlines()
            for line in content:
                key = line.split('=')[0]
                value = line.split('=')[1]

                # Corrective measurements because of Python standards
                try:
                    if value.lower() == 'true':
                        value = True
                    if value.lower() == 'false':
                        value = False
                except AttributeError:
                    pass

                self.set(key, value)
