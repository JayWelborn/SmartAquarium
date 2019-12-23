class ThermometerRegistrationError(ValueError):
    """Error for when thermometer registration fails.

    Should be raised when provided incorrect thermomter ID.

    Wrapper of Value Error class with more verbose name.
    """


class ThermometerCreationError(ValueError):
    """Error for when creating a thermometer fails.

    Should be raised when attempting to create thermometer with temperature
    readings.

    Wrapper of ValueError with more verbose name
    """
