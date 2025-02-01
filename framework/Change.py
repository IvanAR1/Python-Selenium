from .Waits import Waits
from .WebDriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from .Actions import Actions
from typing import Tuple

class Change(Actions, Waits):
    def toFrame(self, element:WebDriver, time:float) -> None:
        self.explicitly(time, self.ec.frame_to_be_available_and_switch_to_it(element))

    def nextPage(self, element:WebElement|Tuple[str, str], seconds:float, time_sleep:float=0) -> None:
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
        self.driver.switch_to.default_content()