import os
import platform
import win32com.client
from selenium import webdriver
from typing import Self, Optional
from libs.path.config_loader import env
from config.browsers import SAVED_ON_LOCAL, BROWSERS 
from selenium.webdriver.common import service as Service
from selenium.webdriver.common.options import ArgOptions
from webdriver_manager.core.os_manager import ChromeType
from libs.path.path_utils import NormalizePathExpandVars
from selenium.webdriver.remote.webdriver import WebDriver as SeleniumWebDriver
from libs.logs import get_log_folder

os.environ["WDM_LOCAL"] = str(SAVED_ON_LOCAL)
class WebDriver():
	"""
	Class to configure and manage a Selenium WebDriver instance.

	Attributes:
		browser (str): 
			The name of the browser to use.
		driver (Optional[SeleniumWebDriver]):
			The Selenium WebDriver instance.
		grid_url (Optional[ChromeType]):
			URL of the Selenium Grid Hub (if running in Grid Mode)
		_chrome_type (ChromeType | None):
			Identifies if the browser is a Chrome-based type.
		
	"""
	browser:str = None
	driver:Optional[SeleniumWebDriver] = None
	grid_url:Optional[str] = env("SELENIUM_GRID_URL")
	_chrome_type:ChromeType = None

	def _set_browser_type(self:Self, browser:str):
		"""
        Determines if the browser is a Chrome.based type and sets the `_chrome_type` attribute.

		Args:
			self (Self):
				class instance
			browser (str):
				Browser name (e.g., 'CHROME', 'GOOGLE', GOOGLE CHROME')
		"""
		browser_aliases = ("GOOGLE", "CHROME", "GOOGLE CHROME")
		if browser.upper() in browser_aliases:
			browser = "GOOGLE"
		self.browser = browser
		self._chrome_type = ChromeType.__dict__.get(browser.upper())

	def _get_browser_specifications(self:Self):
		"""Retrieves browser-specific settings such as WebDriver, manager, options, and service.

		Args:
			self (Self):
				class instance
			browser (str):
				browser (str): Browser name.
		Returns:
			tuple: Specifications including web driver, manager, options, and service.
		"""
		return BROWSERS.get( self.browser.upper(), (None, None, None, None) )

	def get_driver(self:Self,
			browser:str= "CHROME",
			binary_path:str|None = env("BINARY_PATH"),
			browser_version:str|None = env("BROWSER_VERSION"),
			required_log:bool = False,
			use_grid:bool = False,
			**kwargs
		)-> SeleniumWebDriver:
		"""
		Initializes and returns a Selenium WebDriver instance.

		Args:
			self (WebDriver):
				Instance of class.
			browser (str|None):
				Browser name (default: 'GOOGLE')
			binary_path (str|None):
				Path of the browser binary, if needed.
			browser_version (str|None):
				Version of the Browser app (recommended if crashed for not found version).
			use_grid:bool (False):
				If True, connects to Selenium Grid.	
			
		Returns
			SeleniumWebDriver:
				Configured WebDriver instance.
		Raises:
			ValueError:
				If the browser is not supported.
		"""
		self._set_browser_type(browser)

		#Changed binary shortcut to binary realpath
		if str(binary_path).rsplit(".", 1)[-1] and "Win" in platform.system():
			shell = win32com.client.Dispatch("WScript.Shell")
			binary_path = shell.CreateShortCut(NormalizePathExpandVars(binary_path)).Targetpath
		else:
			binary_path = os.path.realpath(NormalizePathExpandVars(binary_path))
		web_driver, manager, options_cls, service_cls = self._get_browser_specifications()
		if not all([web_driver, manager, options_cls, service_cls]):
			raise ValueError(f"El navegador {self.browser} no está soportado")
		# Install WebDriver
		driver_path:str = manager(chrome_type=self._chrome_type, driver_version=browser_version).install() \
			if self._chrome_type else manager(version=browser_version).install()
		options:ArgOptions = options_cls()
		if binary_path:
			options.binary_location = NormalizePathExpandVars(binary_path)
		if use_grid and self.grid_url:
			options.add_argument("--no-sandbox")
			return webdriver.Remote(command_executor=self.grid_url, options=options, **kwargs)

		service:Service = service_cls(driver_path, log_output=(get_log_folder("selenium"), None)[not required_log])
		# Configure browser-specific options
		if self.browser.lower() == "opera":
			options.add_argument("--remote-allow-origins=*")
			options.add_experimental_option('w3c', True)
		return web_driver(service=service, options=options)

	@classmethod
	def initialize_driver(cls:Self, browser:str = env("BROWSER"), log:bool = False) -> SeleniumWebDriver:
		"""
		Initialize the Selenium WebDriver instance as a singleton instance.

		Args:
			cls (Self):
				Instance of class (not required)
			browser (str):
				Browser to be used (default: value from env 'BROWSER')

		Returns:
			SeleniumWebDriver:
				Singleton instance of WebDriver
		"""
		if cls.driver is None:
			cls.driver = WebDriver().get_driver(browser, required_log=log)
		return cls.driver
	
	def factory_main(*objs:Self):
		"""
		Execute 'main()' method of multiple instances

		Args:
			objs ((Self|list[Self])):
				One or more class instances.
		"""
		for obj in objs:
			obj.main()

	def __del__(self:Self):
		"""
		Ensures that the WebDriver instance is properly closed when the object is deleted.
		"""
		if isinstance(self.driver, SeleniumWebDriver):
			self.driver.quit()