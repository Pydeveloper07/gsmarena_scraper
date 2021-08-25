from abc import ABC, abstractmethod
from bs4 import BeautifulSoup, NavigableString
import urllib.request
import requests
import re
from .dicts import *


class Scraper(ABC):
    def __init__(self, url, main_url):
        self.url = url
        self.main_url = main_url
        super().__init__()

    def get_soup(self, headers, proxy):
        if proxy:
            source = requests.get(self.url, headers=headers, proxies=proxy).text
        else:
            source = requests.get(self.url, headers=headers).text
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
        self.table_blocks = {}
        self.img_url = ""

    def parse_and_get_result(self, main_content):
        self.__init_table_blocks(main_content)
        self.__collect_phone_details(main_content)
        self.__collect_image(main_content)
        # self.__download_image()

        return self.phone

    def __download_image(self):
        try:
            urllib.request.urlretrieve(self.img_url, f"files/images/{self.phone['name']}")
        except Exception:
            pass

    def __collect_image(self, content):
        image_block = content.find("div", class_="specs-photo-main")
        self.img_url = image_block.find("img")["src"]
        self.phone.update({"image_url": self.img_url})

    def __init_table_blocks(self, content):
        block = content.find("div", id="specs-list")
        all_tables = block.find_all("table")
        for table in all_tables:
            header = str(table.find("th").text)
            self.table_blocks[header.lower()] = table

    def __collect_phone_details(self, content):
        self.__collect_name_data(content)
        self.__collect_network_data(self.table_blocks.get("network", None))
        self.__collect_launch_data(self.table_blocks.get("launch", None))
        self.__collect_body_data(self.table_blocks.get("body", None))
        self.__collect_display_data(self.table_blocks.get("display", None))
        self.__collect_platform_data(self.table_blocks.get("platform", None))
        self.__collect_memory_data(self.table_blocks.get("memory", None))
        self.__collect_main_camera_data(self.table_blocks.get("main camera", None))
        self.__collect_selfie_camera_data(self.table_blocks.get("selfie camera", None))
        self.__collect_sound_data(self.table_blocks.get("sound", None))
        self.__collect_comms_data(self.table_blocks.get("comms", None))
        self.__collect_features_data(self.table_blocks.get("features", None))
        self.__collect_battery_data(self.table_blocks.get("battery", None))
        self.__collect_misc_data(self.table_blocks.get("misc", None))

    def __collect_name_data(self, main_content):
        data = NameData()
        if not main_content:
            self.phone.update({
                "name": "",
            })
            return
        try:
            name = main_content.find("h1", class_="specs-phone-name-title").text
        except Exception:
            name = ""
        data["name"] = name
        self.phone.update(data)

    def __collect_network_data(self, table_content):
        data = NetworkData()
        if not table_content:
            self.phone.update({
                "network_technology": "",
            })
            return
        try:
            network_row = table_content.find_all("tr")[0]
            try:
                network_technology = network_row.find("td", class_="nfo").a.text
            except Exception:
                network_technology = ""
        except Exception:
            network_technology = ""
        data["network_technology"] = network_technology
        self.phone.update(data)

    def __collect_launch_data(self, table_content):
        data = LaunchData()
        if not table_content:
            self.phone.update({
                "announced": "",
                "status": ""
            })
            return
        try:
            announced = table_content.find("td", {"data-spec": "year"}).text
        except Exception:
            announced = ""
        try:
            status = table_content.find("td", {"data-spec": "status"}).text
        except Exception:
            status = ""
        data["announced"] = announced
        data["status"] = status
        self.phone.update(data)

    def __collect_body_data(self, table_content):
        data = BodyData()
        if not table_content:
            self.phone.update({
                "dimensions": "",
                "weight": 0,
                "build": "",
                "sim": ""
            })
            return
        try:
            dimensions = table_content.find("td", {"data-spec": "dimensions"}).text
        except Exception:
            dimensions = ""
        try:
            weight = float(re.findall("[0-9]+", table_content.find("td", {"data-spec": "weight"}).text)[0])
        except Exception:
            weight = 0
        try:
            build = table_content.find("td", {"data-spec": "build"}).text
        except Exception:
            build = ""
        try:
            sim = table_content.find("td", {"data-spec": "sim"}).text
        except Exception:
            sim = ""

        data["dimensions"] = dimensions
        data["weight"] = weight
        data["build"] = build
        data["sim"] = sim
        self.phone.update(data)

    def __collect_display_data(self, table_content):
        data = DisplayData()
        if not table_content:
            self.phone.update({
                "type": "",
                "size": "",
                "resolution": "",
                "protection": ""
            })
            return
        try:
            display_type = table_content.find("td", {"data-spec": "displaytype"}).text
        except Exception:
            display_type = ""
        try:
            size = table_content.find("td", {"data-spec": "displaysize"}).text
        except Exception:
            size = ""
        try:
            resolution = table_content.find("td", {"data-spec": "displayresolution"}).text
        except Exception:
            resolution = ""
        try:
            protection = table_content.find("td", {"data-spec": "displayprotection"}).text
        except Exception:
            protection = ""

        data["type"] = display_type
        data["size"] = size
        data["resolution"] = resolution
        data["protection"] = protection
        self.phone.update(data)

    def __collect_platform_data(self, table_content):
        data = PlatformData()
        if not table_content:
            self.phone.update({
                "os": "",
                "chipset": [],
                "cpu": [],
                "gpu": []
            })
            return
        try:
            os = table_content.find("td", {"data-spec": "os"}).text
        except Exception:
            os = ""
        try:
            chipset = []
            chipset_children = table_content.find("td", {"data-spec": "chipset"}).children
            for child in chipset_children:
                if isinstance(child, NavigableString):
                    chipset.append(child)
        except Exception:
            chipset = []
        try:
            cpu = []
            cpu_children = table_content.find("td", {"data-spec": "cpu"}).children
            for child in cpu_children:
                if isinstance(child, NavigableString):
                    cpu.append(child)
        except Exception:
            cpu = []
        try:
            gpu = []
            gpu_children = table_content.find("td", {"data-spec": "gpu"}).children
            for child in gpu_children:
                if isinstance(child, NavigableString):
                    gpu.append(child)
        except Exception:
            gpu = []

        data["os"] = os
        data["chipset"] = chipset
        data["cpu"] = cpu
        data["gpu"] = gpu
        self.phone.update(data)

    def __collect_memory_data(self, table_content):
        data = MemoryData()
        if not table_content:
            self.phone.update({
                "card_slot": "",
                "internal_memory": ""
            })
            return
        try:
            card_slot = table_content.find("td", {"data-spec": "memoryslot"}).text
        except Exception:
            card_slot = ""
        try:
            internal_memory = table_content.find("td", {"data-spec": "internalmemory"}).text
        except Exception:
            internal_memory = ""

        data["card_slot"] = card_slot
        data["internal_memory"] = internal_memory
        self.phone.update(data)

    def __collect_main_camera_data(self, table_content):
        data = MainCameraData()
        if not table_content:
            self.phone.update({
                "mc_type": "",
                "mc_details": [],
                "mc_features": "",
                "mc_video": ""
            })
            return
        try:
            mc_type = table_content.find("td", class_="ttl").a.text
        except Exception:
            mc_type = ""
        try:
            mc_details = []
            details_children = table_content.find("td", {"data-spec": "cam1modules"}).children
            for child in details_children:
                if isinstance(child, NavigableString):
                    mc_details.append(child)
        except Exception:
            mc_details = []
        try:
            mc_features = table_content.find("td", {"data-spec": "cam1features"}).text
        except Exception:
            mc_features = ""
        try:
            mc_video = table_content.find("td", {"data-spec": "cam1video"}).text
        except Exception:
            mc_video = ""

        data["mc_type"] = mc_type
        data["mc_details"] = mc_details
        data["mc_features"] = mc_features
        data["mc_video"] = mc_video
        self.phone.update(data)

    def __collect_selfie_camera_data(self, table_content):
        data = SelfieCameraData()
        if not table_content:
            self.phone.update({
                "sc_type": "",
                "sc_details": [],
                "sc_features": "",
                "sc_video": ""
            })
            return
        try:
            sc_type = table_content.find("td", class_="ttl").a.text
        except Exception:
            sc_type = ""
        try:
            sc_details = []
            details_children = table_content.find("td", {"data-spec": "cam2modules"}).children
            for child in details_children:
                if isinstance(child, NavigableString):
                    sc_details.append(child)
        except Exception:
            sc_details = []
        try:
            sc_features = table_content.find("td", {"data-spec": "cam2features"}).text
        except Exception:
            sc_features = ""
        try:
            sc_video = table_content.find("td", {"data-spec": "cam2video"}).text
        except Exception:
            sc_video = ""

        data["sc_type"] = sc_type
        data["sc_details"] = sc_details
        data["sc_features"] = sc_features
        data["sc_video"] = sc_video
        self.phone.update(data)

    def __collect_sound_data(self, table_content):
        data = SoundData()
        if not table_content:
            self.phone.update({
                "loudspeaker": "",
                "jack": ""
            })
            return
        try:
            loudspeaker_row = table_content.find_all("tr")[0]
            loudspeaker = loudspeaker_row.find("td", class_="nfo").text
        except Exception:
            loudspeaker = ""
        try:
            jack_row = table_content.find_all("tr")[1]
            jack = jack_row.find("td", class_="nfo").text
        except Exception:
            jack = ""

        data["loudspeaker"] = loudspeaker
        data["jack"] = jack
        self.phone.update(data)

    def __collect_comms_data(self, table_content):
        data = CommsData()
        if not table_content:
            self.phone.update({
                "wlan": "",
                "bluetooth": "",
                "gps": "",
                "nfs": "",
                "radio": "",
                "usb": ""
            })
            return
        try:
            wlan = table_content.find("td", {"data-spec": "wlan"}).text
        except Exception:
            wlan = ""
        try:
            bluetooth = table_content.find("td", {"data-spec": "bluetooth"}).text
        except Exception:
            bluetooth = ""
        try:
            gps = table_content.find("td", {"data-spec": "gps"}).text
        except Exception:
            gps = ""
        try:
            nfc = table_content.find("td", {"data-spec": "nfc"}).text
        except Exception:
            nfc = ""
        try:
            radio = table_content.find("td", {"data-spec": "usb"}).text
        except Exception:
            radio = ""
        try:
            usb = table_content.find("td", {"data-spec": "usb"}).text
        except Exception:
            usb = ""

        data["wlan"] = wlan
        data["bluetooth"] = bluetooth
        data["gps"] = gps
        data["nfc"] = nfc
        data["radio"] = radio
        data["usb"] = usb
        self.phone.update(data)

    def __collect_features_data(self, table_content):
        data = FeaturesData()
        if not table_content:
            self.phone.update({
                "sensors": "",
                "features_other": []
            })
            return
        try:
            sensors = table_content.find("td", {"data-spec": "sensors"}).text
        except Exception:
            sensors = ""
        try:
            features_other = []
            features_other_children = table_content.find("td", {"data-spec": "featuresother"}).children
            for child in features_other_children:
                if isinstance(child, NavigableString):
                    features_other.append(child)
        except Exception:
            features_other = []

        data["sensors"] = sensors
        data["features_other"] = features_other
        self.phone.update(data)

    def __collect_battery_data(self, table_content):
        data = BatteryData()
        if not table_content:
            self.phone.update({
                "battery_type": "",
                "charging": [],
                "stand_by": "",
                "music_play": ""
            })
            return
        try:
            battery_type = table_content.find("td", {"data-spec": "batdescription1"}).text
        except Exception:
            battery_type = ""
        try:
            charging = []
            charging_row = table_content.find_all("tr")[1]
            charging_children = charging_row.find("td", class_="nfo").children
            for child in charging_children:
                if isinstance(child, NavigableString):
                    charging.append(child)
        except Exception:
            charging = []
        try:
            stand_by = table_content.find("td", {"data-spec": "batstandby1"}).text
        except Exception:
            stand_by = ""
        try:
            music_play = table_content.find("td", {"data-spec": "batmusicplayback1"}).text
        except Exception:
            music_play = ""

        data["battery_type"] = battery_type
        data["charging"] = charging
        data["stand_by"] = stand_by
        data["music_play"] = music_play
        self.phone.update(data)

    def __collect_misc_data(self, table_content):
        data = MiscData()
        if not table_content:
            self.phone.update({
                "colors": "",
                "models": "",
                "price": ""
            })
            return
        try:
            colors = table_content.find("td", {"data-spec": "colors"}).text
        except Exception:
            colors = ""
        try:
            models = table_content.find("td", {"data-spec": "models"}).text
        except Exception:
            models = ""
        try:
            price = table_content.find("td", {"data-spec": "price"}).text
        except Exception:
            try:
                price = table_content.find("td", {"data-spec": "price"}).a.text
            except Exception:
                price = 0

        data["colors"] = colors
        data["models"] = models
        data["price"] = price
        self.phone.update(data)
        
