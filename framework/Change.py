from .Waits import Waits;
from .WebDriver import WebDriver;
from selenium.webdriver.support import expected_conditions as EC;
from .Actions import Actions;

class Change(Actions, Waits):
    def toFrame(self, element:WebDriver, time:float) -> None:
        self.explicitly(time, EC.frame_to_be_available_and_switch_to_it(element));

    def nextPage(self, element:WebDriver, seconds:float) -> None:
        actualTabs = set(self.driver.window_handles);
        self.click(element);
        self.explicitly(seconds, EC.number_of_windows_to_be(len(actualTabs)+1));
        newWindow = (set(self.driver.window_handles) - actualTabs).pop();
        self.driver.switch_to.window(newWindow);

    def defaultContent(self) -> None:
        self.driver.switch_to.default_content();