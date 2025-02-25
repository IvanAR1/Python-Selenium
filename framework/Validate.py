from selenium.webdriver.common.by import By
from framework import Actions, WebDriver

class Validate(Actions):
    """Validate if element is on browser

    Inherince of:
        Actions: Take an action on browser.
    """
    @classmethod
    def Xpath(self, xpath)->bool:
        """Validate if element exist by xpath. 

        Args:
            xpath (_type_): Element to find by xpath. 

        Returns:
            bool: If element is found.
        """
        return self.Any(self.XPATH, xpath)

    @classmethod
    def Id(self, id)->bool:
        """Validate if element exist by ID. 

        Args:
            xpath (_type_): Element to find by id. 

        Returns:
            bool: If element is found.
        """
        return self.Any(self.ID, id)

    @classmethod
    def Any(self, By:By, element:WebDriver)->bool:
        """Validate if element exist with By strategy.

        Args:
            By (By): By strategy.
            element (WebDriver): Found element.

        Returns:
            bool: If element is found.
        """
        try:
            if len(self.findElements(By, element) ) > 0:
                return True
            return False
        except Exception:
            return False