#!/usr/bin/env python
from errors import *

import requests
import os
import json


class QrGenerator:
    """
    QRGenerator Class, which wraps the API of qr-code-generator.com

    Parameters
    ----------
    token : str
        API Access Token, which can be retrieved from https://app.qr-code-generator.com/api/?from=options
        Set to '.env' to load access-token from environment (export ACCESS_TOKEN=your token here)

    **kwargs
        A way to directly set the qr generation settings to the generator.
        >>> t = QrGenerator(None, qr_code_text='TEST')
        >>> t.get_option('qr_code_text')
        'TEST'

    Attributes
    ----------
    data : dict
        Dictionary with the data object used in the POST request to the API

    config : dict
        Configuration settings for the project. Can be updated to change workings of the program.

    output_filename : str
        Filename to output to. Should not include extension. Can either be changed directly or gets updated in the request function.
    """
    def __init__(self, token=None, **kwargs):
        self.data = {
            'access-token': None,
            'qr_code_text': "SPERZIEBONEN",
            'image_format': 'SVG',
            'image_width': 500,
            'download': 0,
            'foreground_color': '#000000',
            'background_color': '#FFFFFF',
            'marker_left_inner_color': '#000000',
            'marker_left_outer_color': '#000000',
            'marker_right_inner_color': '#000000',
            'marker_right_outer_color': '#000000',
            'marker_bottom_inner_color': '#000000',
            'marker_bottom_outer_color': '#000000',
            'marker_left_template': 'version1',
            'marker_right_template': 'version1',
            'marker_bottom_template': 'version1',
            'qr_code_logo': 'no-logo',
            'frame_color': '#000000',
            'frame_text': None,
            'frame_text_color': '#ffffff',
            'frame_icon_name': 'app',
            'frame_name': 'no-frame',
        }
        self.config = {
            'API_URI': 'https://api.qr-code-generator.com/v1/create?',
            'FORCE_OVERWRITE': False,
            'REQUIRED_PARAMETERS': [
                'access-token',
                'qr_code_text'
            ],
            'OUT_FOLDER': 'out',
            'OUTPUT_FOLDER': 'kfc',
        }
        self.output_filename = None

        if token:
            if token == '.env':
                self.data['access-token'] = os.environ['ACCESS_TOKEN']
            else:
                self.data['access-token'] = token

        for key, value in kwargs.items():
            self.set_option(key, value)

        if not os.path.exists(self.config['OUT_FOLDER']):
            os.mkdir(self.config['OUT_FOLDER'])

        if not os.path.exists(self.config['OUT_FOLDER'] + '/' + self.config['OUTPUT_FOLDER']):
            os.mkdir(self.config['OUT_FOLDER'] + '/' + self.config['OUTPUT_FOLDER'])

    def set_option(self, key, value):
        """
        Setter for the data dictionary object. If exists, updates the key value.
        >>> t = QrGenerator()
        >>> t.set_option('qr_code_text', 'Job')
        >>> t.get_option('qr_code_text')
        'Job'

        Parameters
        ----------
        key : str
            The key that we want to change
        value : str
            The value we want to update the key to

        Raises
        ------
        ParameterNotExistsError
            The parameter that is requested to be updated does not exist

        Returns
        -------
        None
        """
        if key not in self.data.keys():
            raise KeyError
        self.data[key] = value

    def get_option(self, key):
        """
        Getter for the data dictionary object. If exists, returns the key value.
        >>> t = QrGenerator()
        >>> t.get_option('qr_code_text') == t.data['qr_code_text']
        True

        >>> t = QrGenerator()
        >>> not t.get_option('xdwdwedewdwede')
        True

        Parameters
        ----------
        key : str
            The key of which the value is requested to be returned

        Returns
        -------
        value : str
            The value of the requested key in the data dictionary
        """
        try:
            return self.data[key]
        except KeyError:
            return None

    def create_query_url(self):
        """
        Generates the query URL which is necessary to retrieve the QR code from the API

        Returns
        -------
        query_url : str
            The URL including querystring that can be used to send the POST request

        """
        query_url = self.config['API_URI']
        for key, value in self.data.items():
            if value:
                if query_url == self.config['API_URI']:
                    query_url = query_url + str(key) + "=" + str(value)
                else:
                    query_url = query_url + "&" + str(key) + "=" + str(value)
        return query_url

    def request(self, file_name=None):
        """
        Requests a QR code from the API with the settings specified in the data object.

        Parameters
        ----------
        file_name : str
            Default None. Used to set the name of the file that should be outputted. Do not give in extension.

        Returns
        -------
        None
        """
        if file_name:
            self.output_filename = file_name

        self.validate()
        url = self.create_query_url()
        req = requests.post(url, data=self.data)
        self.handle_response(req)
        self.cleanup()

    def handle_response(self, response):
        """
        Handles the response from the API by checking status code and choosing whether or not to call error handling.

        Parameters
        ----------
        response : Response
            The full Response object that was retrieved from the API

        Returns
        -------
        None
        """
        if not response.status_code == 200:
            self.handle_api_error(response)
        self.to_output_file(response.text)

    def cleanup(self):
        """
        Resets the file name after receiving a QR code, so that file is never overwritten when not called for by user.
        >>> t = QrGenerator()
        >>> t.output_filename = 'Radishes'
        >>> print(t.output_filename)
        Radishes
        >>> t.cleanup()
        >>> print(t.output_filename)
        None

        Returns
        -------
        None
        """
        self.output_filename = None

    def to_output_file(self, content):
        """
        Writes the content of the response to the output file.

        Parameters
        ----------
        content : Response.text
            The text content of the response that was sent by the API.

        Raises
        ------
        FileExistsError
            Output file does already exist and cannot be overwritten due to config settings.

        Returns
        -------
        None
        """
        file = self.config['OUT_FOLDER'] + '/' + self.config['OUTPUT_FOLDER'] + '/' + self.output_filename + '.' + self.data['image_format'].lower()
        if os.path.exists(file) and not os.stat(file).st_size == 0 and not self.config['FORCE_OVERWRITE']:
            raise FileExistsError
        with open(file, 'w') as f:
            f.writelines(content)

    @staticmethod
    def handle_api_error(response):
        """
        Error handling for status codes sent back by the API.

        Parameters
        ----------
        response : Response
            The full Response object that was returned by the API.

        Raises
        ------
        InvalidCredentialsError
            The access-token has been rejected by the API and is considered invalid.
        FileNotFoundError
            The requested API URI does not exist.
        UnprocessableRequestError
            The request could not be processed by the API.
        MonthlyRequestLimitExceededError
            The current authenticated user has run out of monthly requests. Either change token, upgrade or wait.

        Returns
        -------
        None
        """
        code = response.status_code
        if code == 401:
            print(os.environ['ACCESS_TOKEN'])
            raise InvalidCredentialsError
        if code == 404:
            raise FileNotFoundError
        if code == 422:
            content = json.loads(response.content)
            for error in content['errors']:
                raise UnprocessableRequestError('Issue with field {}: {}'.format(error['field'], error['message']))
        if code == 429:
            raise MonthlyRequestLimitExceededError
        raise UnknownApiError("An unhandled API exception occurred")

    def validate(self):
        """
        Validates the content in the request client-side to avoid getting errors processing.
        Since the API does not give back an error on missing parameter, we validate this to avoid pointless requests.

        Raises
        ------
        FileNotFoundError
            Either the combination of OUT_FOLDER and OUTPUT_FOLDER does not exist, or there was no filename to write to.
        MissingRequiredParameterError
            The request is sent with a missing parameter, which leads to an error on the server side.

        Returns
        -------
        None
        """
        if not self.config['OUT_FOLDER'] or not self.config['OUTPUT_FOLDER']:
            raise FileNotFoundError

        if not self.output_filename:
            raise FileNotFoundError

        for key, value in self.data.items():
            if key in self.config['REQUIRED_PARAMETERS'] and not value:
                raise MissingRequiredParameterError(key)
