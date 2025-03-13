from typing import Self, List
from .WebDriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains, AnyDevice

class Actions(WebDriver, By):
    """Take an action on browser.

    Inherince of:
        WebDriver
        By

    Attributes:
        keys (Keys): Set of special keys codes.
        web_element (WebElement): Use for typing with WebElement
    """

    keys:Keys = Keys
    web_element = WebElement

    @property
    def actions_chains(self:Self) -> property:
        """Get property (ActionChains class)

        Args:
            self (Self): Actions class 

        Returns:
            property: ActionChains class
        """
        return ActionChains(self.driver)
    
    @actions_chains.setter
    def actions_chains(self:Self, driver:WebDriver=None, duration:int = 250, devices:list[AnyDevice] | None = None)-> ActionChains:
        """Set actions_chains property

        Args:
            self (Self): Actions class
            driver (WebDriver, optional): Driver current. Defaults to None.
            duration (int, optional): Duration to get action chains. Defaults to 250.
            devices (list[AnyDevice] | None, optional): Device to execute. Defaults to None.

        Returns:
            ActionChains: _description_
        """
        return ActionChains(driver or self.driver, duration, devices)

    @classmethod
    def findElement(self:Self, by:By|str = By.ID, element:str = "") -> WebElement:
        """Find an element given a By strategy and locator.

        :Usage:
            element = driver.find_element(By.ID, 'foo')

        Args:
            self (Self): Actions class.
            by (By | str, optional): By strategy. Defaults to By.ID.
            element (str, optional): Element to find. Defaults to "".

        Returns:
            WebElement: A new WebElement.
        """
        return self.driver.find_element(by, element)
    
    @classmethod
    def findElements(self:Self, by:By|str = By.ID, element:str = "") -> List[WebElement]:
        """Find elements given a By strategy and locator.

        Args:
            self (Self): Actions class.
            by (By | str, optional): By strategy. Defaults to By.ID.
            element (str, optional): Element to find. Defaults to "".

        Returns:
            List[WebElement]: A WebElement list.
        """
        return self.driver.find_elements(by, element)

    @classmethod
    def click(self:Self, element:WebElement) -> WebElement:
        """Clicks the element.

        Args:
            self (Self): Actions class.
            element (WebElement): Found element.

        Returns:
            WebElement: Element given.
        """
        element.click()
        return element
    
    @classmethod
    def clickByScript(self:Self, element:WebElement) -> WebElement:
        """Excecute a script with element given.

        Args:
            self (Self): Actions class
            element (WebElement): Found element.

        Returns:
            WebElement: Element given.
        """
        self.driver.execute_script("arguments[0].click();", element)
        return element
    
    @classmethod
    def doubleClick(self:Self, element:WebElement|None = None) -> None:
        """Double click the element.

        Args:
            self (Self): Actions class.
            element (WebElement | None, optional): Found Element. Defaults to None.
        """
        Actions.actions_chains.fget(self).double_click(on_element=element).perform()
    
    @classmethod
    def moveToElement(self:Self, element:WebElement, clickeable:bool=True) -> None:
        """Move to element given.

        Args:
            self (Self): Actions class.
            element (WebElement): Found Element.
            clickeable (bool, optional): If will click on element. Defaults to True.
        """
        if clickeable:
            Actions.actions_chains.fget(self).move_to_element(element).click().perform()
        else:
            Actions.actions_chains.fget(self).move_to_element(element).perform()

    @classmethod
    def sendKeys(self:Self, element:WebElement, *keys:str|Keys) -> None:
        """Simulates typing into the element. 

        Args:
            self (Self): Actions class.
            element (WebElement): Found Element.
            *keys (str | Keys): Values to send.
        """
        try:
            Actions.actions_chains.fget(self).click(on_element=element).send_keys(*keys).perform()
        except Exception as e:
            if "cyclic object value" in str(e).lower():
                element.send_keys(*keys)

    @classmethod
    def scrollElement(self:Self, element:WebDriver) -> WebElement:
        """Scroll to element. Similar with moveToElement, but this is done by script.

        Args:
            self (Self): Actions class.
            element (WebDriver): Found element.

        Returns:
            WebElement: Element given.
        """
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        return element

    @classmethod
    def selectOptionByValue(self:Self, element:WebElement, value:str) -> WebElement|None:
        """Select in <option> tag by value attribute.

        Args:
            self (Self): Actions class.
            element (WebElement): Found element.
            value (str): Value to select.

        Returns:
            WebElement: Element given
            None: If don't selected
        """
        select_box = Select(element)
        selects = [option.get_attribute("value") for option in select_box.options]
        for option in selects:
            if option == value:
                select_box.select_by_value(value)
                return element
    
    @classmethod
    def selectOptionByText(self:Self, element:WebElement, text:str):
        """Select in <option> tag by text.

        Args:
            self (Self): Actions class.
            element (WebElement): Found element.
            value (str): Text to select.

        Returns:
            WebElement: Element given
            None: If don't selected
        """
        select_box = Select(element)
        selects = [option.text for option in select_box.options]
        for option in selects:
            if option == text:
                select_box.select_by_visible_text(text)
                return element
            
    @classmethod
    def closeAllWindowsExceptOne(self, page_not_close:str = None):
        """Close all browser windows, except page where driver is working or the specified page.

        Args:
            page_not_close (str, optional): Page to specific. Defaults to None.
        """
        page_not_close = (self.driver.current_window_handle, page_not_close)[page_not_close is not None]
        for handle in self.driver.window_handles:
            if handle != page_not_close:
                self.driver.switch_to.window(handle)
                self.driver.close()
        self.driver.switch_to.window(page_not_close)