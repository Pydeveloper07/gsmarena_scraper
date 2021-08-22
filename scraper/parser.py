from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import requests
import re


class Scraper(ABC):
    def __init__(self, url, main_url):
        self.url = url
        self.main_url = main_url
        super().__init__()

    def get_soup(self):
        source = requests.get(self.url).text
        return BeautifulSoup(source, "lxml")

    @abstractmethod
    def parse_and_get_result(self, main_content):
        pass


class BrandsScraper(Scraper):
    def __init__(self, url, main_url):
        super().__init__(url, main_url)
        self.brands = []

    def parse_and_get_result(self, main_content):
        all_tds = self.__get_tds(main_content)
        for td in all_tds:
            processed_data = self.__process_data(td)
            self.brands.append(processed_data)
        return self.brands

    @staticmethod
    def __get_tds(content):
        return content.find_all("td")

    def __process_data(self, td):
        url = td.find("a")["href"]
        name = str(td.find("a").next)
        devices = int(re.findall("[0-9]+", td.find("a").text)[0])
        return dict(name=name, devices=devices, url=self.main_url + url)


class PhonesUrlScraper(Scraper):
    def __init__(self, url, main_url):
        super().__init__(url, main_url)
        self.phone_urls = []

    def parse_and_get_result(self, main_content):
        list_items = self.__get_list_items(main_content)
        self.__collect_phone_urls(list_items)
        return self.phone_urls

    @staticmethod
    def __get_list_items(content):
        return content.find_all("li")

    def __collect_phone_urls(self, list_items):
        for item in list_items:
            url = item.find("a")["href"]
            self.phone_urls.append(self.main_url + url)


class PhoneScraper(Scraper):
    def __init__(self, url, main_url):
        super().__init__(url, main_url)
        self.phone = {}
        self.img_url = ""

    def parse_and_get_result(self, main_content):
        self.__collect_image(main_content)
        self.__collect_phone_details(main_content)

        return self.phone

    def __collect_image(self, content):
        image_block = content.find("div", class_="specs-photo-main")
        self.img_url = image_block.find("img")["src"]

    def __collect_phone_details(self, content):
        block = content.find("div", id="specs-list")
        
