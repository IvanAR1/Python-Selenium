import time
from typing import TypeVar
from typing import Callable
from .WebDriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

T = TypeVar("T")
class Waits(WebDriver):
    ec:EC = EC

    @classmethod
    def implicitly(self, time_to_wait:float) -> None:
        """
        Sets a sticky timeout to implicitly wait for an element to be found, or a command to complete.
        This method only needs to be called one time per session. To set the timeout for calls to execute_async_script,
        see set_script_timeout.

        Params:
            time_to_wait:
                Amount of time to wait (in seconds)
        """
        self.driver.implicitly_wait(time_to_wait)

    @classmethod
    def explicitly(self, timeout:float, ec:EC, errorMessage:str = "", driver:WebDriver|WebElement = None) -> T:
        """
        Calls the method provided with the driver as an argument until the return value does not evaluate to ``False``.

        Params:
            timeout:
                Number of seconds before timing out
            method (callable(EC)):
                callable
            message:
                optional message for TimeoutException | Exception

        Returns:
            T:
                the result of the last call to method

        raises:
            TimeoutException (selenium.common.exceptions):
                if timeout occurs
            Exception:
                any error ocurred
        """
        try:
            return WebDriverWait(driver or self.driver, timeout).until(ec, message=errorMessage)
        except:
            returnValues = (False, errorMessage)[errorMessage != ""]
            return returnValues

    @classmethod
    def sleep(self, seconds:float) -> None:
        """
        Delay execution for a given number of seconds. The argument may be a floating point number for
        subsecond precision.

        Params:
            seconds (float):
                Time in seconds for sleep
        """
        time.sleep(seconds)
    
    @classmethod
    def displayedElement(self, element:WebElement) -> bool:
        """
        Delay execution for displayed element.
        Params:
            element (WebElement):
        
        Return:
            True:
                If element is displayed
        """
        while True:
            try:
                if(element.is_displayed()):    
                    return True
            except:
                return True

    @classmethod
    def forAttempt(self, seconds:float, attempts:int, condition:bool|Callable) -> bool:
        """
        Delay execution of a condition. Stops delay if time runs out

        Params:
            seconds (float):
                Time in seconds for sleep
            attemts (int):
                Attempts to fulfill the condition
            condition (bool):
                Condition
        """
        while attempts > 0:
            response = condition if isinstance(condition, bool) else condition()
            if response:
                return response
            time.sleep(seconds)
            attempts -= 1
        return