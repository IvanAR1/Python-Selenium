from .WebDriver import WebDriver
from typing import Self, List, Any
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains, AnyDevice

class Actions(WebDriver, By):
    webElement:WebElement = WebElement
    keys = Keys

    @property
    def actions_chains(self:Self) -> property:
        return ActionChains(self.driver)
    
    @actions_chains.setter
    def actions_chains(self:Self, driver:WebDriver=None, duration:int = 250, devices:list[AnyDevice] | None = None)-> ActionChains:
        return ActionChains(driver or self.driver, duration, devices)

    @classmethod
    def findElement(self:Self, by:By|str = By.ID, element:str = "") -> WebElement:
        return self.driver.find_element(by, element)
    
    @classmethod
    def findElements(self:Self, by:By|str = By.ID, element:str = "") -> List[WebElement]:
        return self.driver.find_elements(by, element)

    @classmethod
    def click(self:Self, element:WebElement) -> WebElement:
        return element.click()
    
    @classmethod
    def clickByScript(self:Self, element:WebDriver) -> Any:
        return self.driver.execute_script("arguments[0].click();", element)
    
    @classmethod
    def doubleClick(self:Self, element:WebElement|None = None) -> None:
        Actions.actions_chains.fget(self).double_click(on_element=element).perform()
    
    @classmethod
    def moveToElement(self:Self, element:WebElement, clickeable:bool=True) -> None:
        if clickeable:
            Actions.actions_chains.fget(self).move_to_element(element).click().perform()
        else:
            Actions.actions_chains.fget(self).move_to_element(element).perform()

    @classmethod
    def sendKeys(self:Self, element:WebElement, keys:str|Keys) -> None:
        Actions.actions_chains.fget(self).click(on_element=element).send_keys(keys).perform()

    @classmethod
    def scrollElement(self:Self, element:WebDriver) -> Any:
        return self.driver.execute_script("arguments[0].scrollIntoView();", element)

    @classmethod
    def selectOptionByValue(self:Self, element:WebElement, value:str):
        select_box = Select(element)
        selects = [option.get_attribute("value") for option in select_box.options]
        for option in selects:
            if option == value:
                return select_box.select_by_value(value)
    
    @classmethod
    def selectOptionByText(self:Self, element:WebElement, text:str):
        select_box = Select(element)
        selects = [option.text for option in select_box.options]
        for option in selects:
            if option == text:
                return select_box.select_by_visible_text(text)
            
    @classmethod
    def closeAllWindowsExceptOne(self, page_not_close:str = None):
        page_not_close = (self.driver.current_window_handle, page_not_close)[page_not_close is not None]
        for handle in self.driver.window_handles:
            if handle != page_not_close:
                self.driver.switch_to.window(handle)
                self.driver.close()
        self.driver.switch_to.window(page_not_close)