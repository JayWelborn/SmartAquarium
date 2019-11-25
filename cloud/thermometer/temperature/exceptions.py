class ThermometerRegistrationError(ValueError):
    """Error for when thermometer registration fails.

    Should be raied when provided incorrect thermomter ID.

    Wrapper of Value Error class with more verbose name.
    """