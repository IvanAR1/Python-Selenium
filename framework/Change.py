from typing import Tuple
from .Waits import Waits
from .Actions import Actions
from .WebDriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

class Change(Actions, Waits):
    """Chage to specific element/window in browser.

    Inherince of:
        Actions: Actions to realize.
        Waits: Waits in specific moment.
    """
    @classmethod
    def toFrame(self, element:WebDriver, time:float) -> None:
        """Switch to specific frame tag.

        Args:
            self: Change class.
            element (WebDriver): Found element.
            time (float): Max time to change.
        """
        self.explicitly(time, self.ec.frame_to_be_available_and_switch_to_it(element))

    @classmethod
    def nextPage(self, element:WebElement|Tuple[str, str], seconds:float, time_sleep:float=0) -> None:
        """Change to next page where driver is working when click on element.

        Args:
            element (WebElement | Tuple[str, str]): Found element if WebElement. Waits with element_to_be_clickable if Tuple
            seconds (float): Number of seconds before timing out (if element is a tuple).
            time_sleep (float, optional): Time to sleep and wait to click on element (if element is a tuple). Defaults to 0.
        """
        actualTabs = set(self.driver.window_handles)
        if isinstance(element, WebElement):
            self.click(element)
        else:
            element = self.explicitly(seconds, self.ec.element_to_be_clickable(element))
            self.sleep(time_sleep)
            self.click(element)
        self.explicitly(seconds, self.ec.number_of_windows_to_be(len(actualTabs)+1))
        newWindow = (set(self.driver.window_handles) - actualTabs).pop()
        self.driver.switch_to.window(newWindow)

    def defaultContent(self) -> None:
        """Change to default content."""
        self.driver.switch_to.default_content()