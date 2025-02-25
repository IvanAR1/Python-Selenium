import os
import platform
import win32com.client
from typing import Self
from selenium import webdriver
from libs.path.loader import env
from selenium.webdriver.remote import webdriver as web
from libs.path.utils.route import NormalizePathExpandVars
from selenium.webdriver.chrome.service import Service as ServiceChrome
from selenium.webdriver.firefox.service import Service as ServiceFirefox

class WebDriver():
	"""
	Configure and run selenium

	Args:
		webelement (WebElement): 
			Object that contains all page's manage.
		browser (str):
			Browser for manager (only Chrome and Firefox)
	"""
	browser:str = None
	driver:web.WebDriver = None

	def _get_options(self:Self, browser:str) -> (webdriver.FirefoxOptions | webdriver.ChromeOptions | None):
		"""
		Get the browser options. 

		Args:
			self (WebDriver): 
				Instance of class. 
			browser (str): 
				Name of the browser (Firefox or Chrome). 

		Returns:
			(FirefoxOptions|ChromeOptions): Options
			(None): If browser isn't support.
		"""
		options = {
			"Firefox": webdriver.FirefoxOptions,
			"Chrome": webdriver.ChromeOptions
		}
		return options.get(browser, None)()

	def _get_service(self:Self, browser:str, fileWebDriver:str) -> (ServiceFirefox | ServiceChrome | None):
		""" 
		Get the service for the browser.

		Args:
			self (WebDriver):
				Instance of class.
			browser (str):
				Name of the browser (Firefox or Chrome).
			fileWebDriver (str):
				Path to the WebDriver executable.
		Returns:
			(ServiceFirefox|ServiceChrome): Service.

			(None): If browser isn't supported
		"""
		services = {
			"Firefox": ServiceFirefox,
			"Chrome": ServiceChrome
		}
		service_class = services.get(browser, None)
		driver = service_class(executable_path=NormalizePathExpandVars(fileWebDriver)) if service_class else None
		return driver

	def _set_driver(self:Self, options:_get_options, service:_get_service, browser:str) -> (web.WebDriver | None):
		"""
		Set the WebDriver instance.

		Args:
			self (WebDriver):
				Instance of class. 
			options (webdriver.FirefoxOptions or webdriver.ChromeOptions):
			 	Options for the browser. 
			service (ServiceFirefox or ServiceChrome): 
				Service for the browser. 
			browser (str):
				Name of the browser (Firefox or Chrome).

		Returns:
			WebDriver: Instance of the WebDriver for Chrome or Firefox.
			
			None: If browser is not supported.
		"""
		drivers = {
			"Firefox": webdriver.Firefox,
			"Chrome": webdriver.Chrome
		}
		driver_class:webdriver.Firefox | webdriver.Chrome = drivers.get(browser, None)
		return driver_class(options=options, service=service) if driver_class else None

	def getDriver(self:Self,
			fileBnLoc:str = env('BINARY_PATH'),
			fileWebDriver:str = env("DRIVER_PATH")
		)-> web.WebDriver:
		"""
		Get the configured WebDriver.

		Args:
			self (WebDriver):
				Instance of class.
			fileBnLoc (str):
				Path to the browser binary.
			fileWebDriver (str):
				Path to the WebDriver executable.

		Returns:
			WebDriver: Configured WebDriver instance.
		
		Raises:
			ValueError: If the browser is not supported.
		"""
		if self.browser not in ["Firefox", "Chrome"]:
			raise ValueError(f"El navegador {self.browser} no está soportado")
		if str(fileBnLoc).rsplit(".", 1)[-1] == "lnk" and "Win" in platform.system():
			shell = win32com.client.Dispatch("WScript.Shell")
			fileBnLoc = shell.CreateShortCut(rf"{NormalizePathExpandVars(fileBnLoc)}").Targetpath
		else:
			fileBnLoc = os.path.realpath(NormalizePathExpandVars(fileBnLoc))
		options = self._get_options(self.browser)
		options.binary_location = fileBnLoc
		service = self._get_service(self.browser, fileWebDriver)
		return self._set_driver(options, service, self.browser)

	@classmethod
	def initialize_driver(self:Self, browser:str = env("BROWSER")):
		"""
		Initialize the Selenium WebDriver instance if it has not already been created.

		Returns:
			webdriver: The singleton instance of Selenium WebDriver
		"""
		if self.driver is None:
			WebDriver.browser = browser
			WebDriver.driver = self.driver = WebDriver().getDriver()
		return self.driver
	
	def factoryMain(*objs:Self):
		
		"""
		Execute the point center

		Args:
			objs ((Self|list[Self])):
				Class(es) instance
		Returns:
			any:
				Anything that you requires
		"""
		for obj in objs:
			obj.main()