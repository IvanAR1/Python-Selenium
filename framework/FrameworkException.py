from selenium.common.exceptions import WebDriverException

class FrameworkException(WebDriverException):
    """Class that Framework uses to raise an exception.

    Inherince of:
        WebDriverException: Default exceptions in WebDriver.
    """
    pass