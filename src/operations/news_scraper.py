import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from src.operations.custom_selenium import CustomSelenium
from selenium.webdriver.support.ui import Select
import re
from src.operations.excel_handler import write_data_to_excel
from uuid import uuid4
from typing import Any
from src.settings import (
    DEFAULT_CATEGORY_NAME,
    DEFAULT_FILTER,
    DEFAULT_SEARCH_PHRASE,
    DEFAULT_URL,
)

EXCEL_PATH = 'output/news.xlsx'


class APNewsScraper(CustomSelenium):
    def __init__(self):
        self.driver = self.set_webdriver()
        self.download_directory = "output"

    def check_money(self, text: str) -> None:
        money_pattern = re.compile(r"\$\d+(?:,\d{3})*(?:\.\d{2})?|\d+ dollars|\d+ USD")
        return bool(money_pattern.search(text))

    def has_image(self, element):
        try:
            return element.find_element(By.CLASS_NAME, "Image")
        except:
            return None

    def download_image(self, url: str, filename: str) -> None:
        original_window = self.driver.current_window_handle
        self.driver.execute_script("window.open('');")
        new_window = [window for window in self.driver.window_handles if window != original_window][0]
        self.driver.switch_to.window(new_window)

        self.open_url(url, filename)
        self.driver.close()
        self.driver.switch_to.window(original_window)

    def search_phrase_on_page(self, search_phrase: str) -> None:
        search_button = self.find_element_located(60, (By.CLASS_NAME, "SearchOverlay-search-button"))
        search_button.click()
        search_input =  self.find_element_located(30, (By.CLASS_NAME, "SearchOverlay-search-input"))
        search_input.send_keys(search_phrase)
        search_input.send_keys(Keys.ENTER)

    def set_category_on_page(self, category_name: str) -> None:
        category_dropdown = self.find_element_clickable(
            60,
            (By.CSS_SELECTOR, 'div.SearchFilter-heading[data-toggle-trigger="search-filter"]')
        )
        category_dropdown.click()
        dropdown_content = self.find_element_visible(30, (By.CLASS_NAME, 'SearchFilter-items')) 
        categories = dropdown_content.find_elements(By.CLASS_NAME, 'CheckboxInput-label')
        for category in categories:
            label = category.find_element(By.CSS_SELECTOR, 'span')
            if label.text.strip().lower() == category_name.lower():
                category.click()
                break

    def set_sorted_filter(self, value_filter: str) -> None:
        dropdown = self.find_element_clickable(30, (By.CLASS_NAME, 'Select-input'))
        select = Select(dropdown)
        select.select_by_value(value_filter)

    def get_search_results(self, search_phrase) -> list[Any]:
        search_results = self.find_all_elements_located(30, (By.CLASS_NAME, "PagePromo"))
        payload = []
        for result in search_results[1:]:
            text = result.find_element(By.CLASS_NAME, "PagePromo-content").text
            image_element = self.has_image(result)
            
            if image_element:
                image_url = image_element.get_attribute("src")
                filename = f"{str(uuid4())}.png"
                if not os.path.exists(f"{self.download_directory}/images/"):
                    os.makedirs(f"{self.download_directory}/images/")

                filename_in_directory = f"{self.download_directory}/images/{filename}"
                self.download_image(image_url, filename_in_directory)
                data = {}
                data['picture_filename'] = filename_in_directory
                text_splited = text.split('\n')
                title = text_splited[0] if len(text_splited)>=1 else ''
                description = text_splited[1] if len(text_splited)>=2 else ''
                
                data['title'] = title
                data['description'] = description
                data['date'] = text_splited[2] if len(text_splited)>=3 else ''
                data['count_phrases'] = title.lower().count(search_phrase.lower()) + description.lower().count(search_phrase.lower())
                data['contain_money'] = self.check_money(text)
                payload.append(data)
                print(f"Image saved: {filename_in_directory}\n")
        return payload
    
    def save_data(self, payload: list[dict[str, Any]], directory: str = EXCEL_PATH):        
        write_data_to_excel(payload, directory)

    def main(self, variables: dict[str, Any]):
        url = variables.get("URL", DEFAULT_URL)
        search_phrase = variables.get("SEARCH_PHRASE", DEFAULT_SEARCH_PHRASE)
        category_name = variables.get("CATEGORY_NAME", DEFAULT_CATEGORY_NAME)
        value_sorted_filter = DEFAULT_FILTER

        self.driver.get(url)
        self.search_phrase_on_page(search_phrase)
        self.set_category_on_page(category_name)
        self.set_sorted_filter(value_sorted_filter)

        payload = self.get_search_results(search_phrase)
        self.save_data(payload)

    def run(self, variables: dict[str, Any]):
        try:
            self.main(variables)
        finally:
            self.driver_quit()
