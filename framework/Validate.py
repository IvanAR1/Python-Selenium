from selenium.webdriver.common.by import By
from framework import Actions, WebDriver

class Validate(Actions):
    @classmethod
    def Xpath(self, xpath)->bool:
        return self.Any(By.XPATH, xpath)

    @classmethod
    def Id(self, id)->bool:
        return self.Any(By.ID, id)

    @classmethod
    def Any(self, By:By, element:WebDriver)->bool:
        try:
            if len(self.findElements(By, element) ) > 0:
                return True
            return False
        except Exception:
            return False