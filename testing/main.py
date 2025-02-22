from framework.WebFacade import WebFacade
from framework import Actions

def execute_from_command_line(action:str):
    if(WebFacade.driver is not None):
        WebFacade.driver.get("https://www.google.com")
        element = WebFacade.driver.find_element(Actions.XPATH, "//textarea[@name='q']")
        WebFacade.get_instance("actions").sendKeys(element, "Selenium with python")
        WebFacade.get_instance("actions").sendKeys(element, Actions.keys.ENTER)
        WebFacade.get_instance("waits").sleep(10)
        WebFacade.driver.quit()
    else:
        print("Execute")