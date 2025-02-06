from selenium import webdriver
from webdriver_manager import chrome, firefox, microsoft, opera
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.ie.service import Service as IEService
from selenium.webdriver.firefox.service import Service as FirefoxService

SAVED_ON_LOCAL:str=str(True)

# webdriver, manager, options, service class
BROWSERS:dict[tuple] = {
    "GOOGLE":(webdriver.Chrome, chrome.ChromeDriverManager, webdriver.ChromeOptions, ChromeService)
    ,"EDGE": (webdriver.Edge, microsoft.EdgeChromiumDriverManager, webdriver.EdgeOptions, EdgeService)
    ,"FIREFOX": (webdriver.Firefox, firefox.GeckoDriverManager, webdriver.FirefoxOptions, FirefoxService)
    ,"INTERNET EXPLORER": (webdriver.Ie, microsoft.IEDriverManager, webdriver.IeOptions, IEService)
    ,"OPERA": (webdriver.Chrome, opera.OperaDriverManager, webdriver.ChromeOptions, ChromeService)
}