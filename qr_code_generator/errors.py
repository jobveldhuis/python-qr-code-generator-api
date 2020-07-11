#!/usr/bin/env python3
class MissingRequiredParameterError(Exception):
    """Raised when a missing required parameter is found, meaning the API cannot generate a QR code."""


class MonthlyRequestLimitExceededError(Exception):
    """Raised when the monthly request limit has been exceeded. Either change key, upgrade or wait."""


class InvalidCredentialsError(Exception):
    """Raised when user provides invalid credentials to the API."""


class UnprocessableRequestError(Exception):
    """Raised when user tries to request something that cannot be given back by the API."""


class UnknownApiError(Exception):
    """Raised when the API gives back an error that is unhandled by the current Python wrapper."""
