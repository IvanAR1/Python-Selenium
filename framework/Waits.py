import time
from .WebDriver import WebDriver
from typing import Callable, Union, List, Literal
from selenium.webdriver.support.wait import T
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class Waits(WebDriver):
    """Timing to wait an element or other actions.

    Inherince of:
        WebDriver

    Attributes:
        ec (EC): Expected conditions.
    """
    ec:EC = EC

    @classmethod
    def implicitly(self, time_to_wait:float) -> None:
        """
        Sets a sticky timeout to implicitly wait for an element to be found, or a command to complete.
        This method only needs to be called one time per session. To set the timeout for calls to execute_async_script,
        see set_script_timeout.

        Args:
            time_to_wait:
                Amount of time to wait (in seconds)
        """
        self.driver.implicitly_wait(time_to_wait)

    @classmethod
    def explicitly(self, timeout:float, ec:EC, errorMessage:str = "", driver:WebDriver|WebElement = None) -> Union[WebElement, List[WebElement], T]:
        """
        Calls the method provided with the driver as an argument until the return value does not evaluate to ``False``.

        Args:
            timeout (float):
                Number of seconds before timing out
            ec (EC):
                Call to method by EC.
            errorMessage (str, optional):
                Optional message for TimeoutException. Defaults to ""
            driver (WebDriver | WebElement, optional): 
                Change driver if necessary. Defaults to None.

        Returns:
            WebElement|List[WebElement]|out:
                The result of the last call to method.
        """
        try:
            return WebDriverWait(driver or self.driver, timeout).until(ec, message=errorMessage)
        except (TimeoutException, Exception):
            returnValues = (False, errorMessage)[errorMessage != ""]
            return returnValues

    @classmethod
    def sleep(self, seconds:float) -> None:
        """
        Delay execution for a given number of seconds. The argument may be a floating point number for
        subsecond precision.

        Args:
            seconds (float):
                Time in seconds for sleep
        """
        time.sleep(seconds)
    
    @classmethod
    def displayedElement(self, element:WebElement) -> Literal[True]:
        """
        Delay execution for displayed element.
        Args:
            element (WebElement): 
        
        Returns:
            Literal[True]:
                If element is displayed
        """
        while True:
            try:
                if(element.is_displayed()):    
                    return True
            except Exception:
                return True

    @classmethod
    def forAttempt(self, seconds:float, attempts:int, condition:bool|Callable[[],bool]) -> bool:
        """
        Delay execution of a condition. Stops delay if time runs out

        Args:
            seconds (float):
                Time in seconds for sleep
            attempts (int):
                Attempts to fulfill the condition
            condition (bool|Callable[[], bool]):
                Condition that must be met.
        """
        while attempts > 0:
            response = condition if isinstance(condition, bool) else condition()
            if response:
                return response
            time.sleep(seconds)
            attempts -= 1
        return