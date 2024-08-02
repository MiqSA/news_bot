from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Tuple
from src.settings import (
    GERERIC_MAX_SLEEP_TIME_SECONDS_INT,
)

class CustomSelenium:
    def set_chrome_options(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument('--disable-web-security')
        options.add_argument("--disable-logging")
        options.add_argument("--start-maximized")
        options.add_argument('--remote-debugging-port=9222')
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.set_capability("pageLoadStrategy", "none") 
        return options

    def set_webdriver(self):
        options = self.set_chrome_options()
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(GERERIC_MAX_SLEEP_TIME_SECONDS_INT+3)
        return self.driver

    def open_url(self, url:str, screenshot:str=None):
        self.driver.get(url)
        if screenshot:
            sleep(GERERIC_MAX_SLEEP_TIME_SECONDS_INT)
            self.driver.get_screenshot_as_file(screenshot)

    def driver_quit(self):
        if self.driver:
            self.driver.quit()
    
    def find_element_located(self, time: int, locator: Tuple[str, str]):
        return WebDriverWait(self.driver, time).until(EC.presence_of_element_located(locator))
    
    def find_element_visible(self, time: int, locator: Tuple[str, str]):
        return WebDriverWait(self.driver, time).until(EC.visibility_of_element_located((locator)))
    
    def find_element_clickable(self, time: int, locator: Tuple[str, str]): 
        return WebDriverWait(self.driver, time).until(EC.element_to_be_clickable(locator))
    
    def find_all_elements_located(self, time: int, locator: Tuple[str, str]):
        return WebDriverWait(self.driver, time).until(EC.presence_of_all_elements_located(locator))