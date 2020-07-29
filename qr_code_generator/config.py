#!/usr/bin/env python3
import yaml


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
        """
        Get the value for a configuration key.

        Parameters
        ----------
        key : str
            The configuration setting you wish to know the value of.

        Returns
        -------
        value : str
            The corresponding value for requested key
        """
        try:
            return self[key]
        except KeyError:
            return None

    def set(self, key, value):
        """
        Set a configuration setting to a value.

        Parameters
        ----------
        key : str
            The key of the setting you wish to set.
        value : str
            The value you wish to set the setting to.

        Raises
        ------
        KeyError
            The setting that is requested to be altered does not exist.

        Returns
        -------
        None
        """
        if key not in self:
            raise KeyError
        else:
            self[key] = value

    def load(self, file):
        """
        Load a .yaml file into the current configuration object.

        Parameters
        ----------
        file : str
            The relative location of the file that should be used to import settings.
        strict : bool
            Whether or not importing should be done strictly or not.

        Raises
        ------
        ValueError
            The selected file is not a .yaml file and cannot be loaded into the configuration.

        Returns
        -------
        None
        """
        extension = file.split('.')[-1]
        if not extension == 'yaml':
            raise ValueError('Configuration file should be a yaml-file.')

        with open(file, "r") as f:
            settings = yaml.load(f)

        for key, value in settings.items():
            self.set(key, value)
