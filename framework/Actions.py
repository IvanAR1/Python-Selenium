from .WebDriver import WebDriver
from typing import Self, List, Any
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains

class Actions(WebDriver, By):
    webElement:WebElement = WebElement

    @classmethod
    def _get_actions(self:Self)-> ActionChains:
        return ActionChains(self.driver)

    @classmethod
    def findElement(self:Self, by:By|str = By.ID, element:str = "") -> WebElement:
        return self.driver.find_element(by, element)
    
    @classmethod
    def findElements(self:Self, by:By|str = By.ID, element:str = "") -> List[WebElement]:
        return self.driver.find_elements(by, element)

    @classmethod
    def click(self:Self, element:WebDriver) -> WebElement:
        return element.click()
    
    @classmethod
    def clickByScript(self:Self, element:WebDriver) -> Any:
        return self.driver.execute_script("arguments[0].click();", element)
    
    @classmethod
    def doubleClick(self:Self, element:WebDriver) -> None:
        self._get_actions().double_click(on_element=element).perform()
    
    @classmethod
    def moveToElement(self:Self, element:WebDriver, clickeable:bool=True) -> None:
        if clickeable:
            self._get_actions().move_to_element(element).click().perform()
        else:
            self._get_actions().move_to_element(element).perform()

    @classmethod
    def sendKeys(self:Self, element:WebDriver, keys:str|Keys) -> None:
        self._get_actions().click(on_element=element).send_keys(keys).perform()

    @classmethod
    def scrollElement(self:Self, element:WebDriver) -> Any:
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    @classmethod
    def selectOptionByValue(self:Self, element:WebDriver, value:str):
        select_box = Select(element)
        selects = [option.get_attribute("value") for option in select_box.options]
        for option in selects:
            if option == value:
                select_box.select_by_value(value)
                break;
    
    @classmethod
    def selectOptionByText(self:Self, element:WebDriver, text:str):
        select_box = Select(element)
        selects = [option.text for option in select_box.options]
        for option in selects:
            if option == text:
                select_box.select_by_visible_text(text)
                break