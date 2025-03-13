from typing import Self
from framework import Actions
from selenium.webdriver.common.by import By

class Validate(Actions):
    """Validate if element is on browser

    Inherince of:
        Actions: Take an action on browser.
    """
    @classmethod
    def Xpath(self:Self, xpath:str)->bool:
        """Validate if element exist by xpath. 

        Args:
            xpath (str): Element to find by xpath. 

        Returns:
            bool: If element is found.
        """
        return self.Any(self.XPATH, xpath)

    @classmethod
    def Id(self:Self, id:str)->bool:
        """Validate if element exist by ID. 

        Args:
            id (str): Element to find by id. 

        Returns:
            bool: If element is found.
        """
        return self.Any(self.ID, id)

    @classmethod
    def Any(self:Self, By:By|str, element:str)->bool:
        """Validate if element exist with By strategy.

        Args:
            By (By|str): By strategy.
            element (str): Element to find.

        Returns:
            bool: If element is found.
        """
        try:
            if len(self.findElements(By, element) ) > 0:
                return True
            return False
        except Exception:
            return False