class MissingRequiredParameterError(Exception):
    pass


class MonthlyRequestLimitExceededError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


class UnprocessableRequestError(Exception):
    pass


class UnknownApiError(Exception):
    pass
