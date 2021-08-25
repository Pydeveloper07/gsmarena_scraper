import time
import sys

import requests
from bs4 import BeautifulSoup

from scraper import BrandsScraper, PhonesUrlScraper, PhoneScraper
from writer import ExcelBrandWriter, ExcelPhoneWriter


def _get_nav_links(soup, main_url):
    links = []
    nav_block = soup.find("div", class_="nav-pages")
    if not nav_block:
        return []
    nav_links = nav_block.find_all("a", href=True)
    for link in nav_links:
        links.append(main_url + link["href"])
    return links


def _parse_and_get_phones(main_url, scrape_urls, headers, proxy):
    parsed_results = []
    index = 1
    total = len(scrape_urls)
    for url in scrape_urls:
        time.sleep(3)
        scraper = PhoneScraper(url, main_url)
        soup = scraper.get_soup(headers, proxy)
        main_content = soup.find('div', class_="main-review")
        parsed_results.append(scraper.parse_and_get_result(main_content))
        sys.stdout.write(f"\r{index}/{total}  ---  ")
        sys.stdout.write("<{0}{1}>".format("%"*index, "_"*(total-index)))
        sys.stdout.flush()
        index += 1

    return parsed_results


def parse_brands_and_write_to_excel(main_url, scrape_url, headers, proxy):
    scraper = BrandsScraper(scrape_url, main_url)
    soup = scraper.get_soup(headers, proxy)
    main_content = soup.find('div', class_="st-text")
    parsed_results = scraper.parse_and_get_result(main_content.table)

    print(f"Number of brands: {len(parsed_results)}")
    writer = ExcelBrandWriter("brands.xlsx", parsed_results)
    writer.write()

    return parsed_results


def parse_brand_phones_and_write_to_excel(main_url, scrape_url, brand_name, headers, proxy):
    source = requests.get(scrape_url, headers=headers, proxies=proxy).text
    temp_soup = BeautifulSoup(source, "lxml")
    nav_links = _get_nav_links(temp_soup, main_url)
    nav_links.append(scrape_url)
    parsed_urls = []
    for nav_link in nav_links:
        time.sleep(3)
        scraper = PhonesUrlScraper(nav_link, main_url)
        soup = scraper.get_soup(headers, proxy)
        main_content = soup.find('div', class_="makers")
        parsed_urls += scraper.parse_and_get_result(main_content.ul)

    print(f"Number of phones ({brand_name}): {len(parsed_urls)}")

    parsed_results = _parse_and_get_phones(main_url, parsed_urls, headers, proxy)

    writer = ExcelPhoneWriter(f"{brand_name}.xlsx", parsed_results)
    writer.write()

    return parsed_results


if __name__ == "__main__":
    url = "https://www.gsmarena.com/"
    brands_url = "https://www.gsmarena.com/makers.php3"
    headers = {
        "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    }
    # proxy = {
    #     "https": "135.148.148.176:8080"
    # }
    proxy = None

    brands = parse_brands_and_write_to_excel(url, brands_url, headers, proxy)
    # for brand in brands:
    #     time.sleep(1)
    # brand = brands[1]
    brands_temp = brands[29:33]
    for i, brand in enumerate(brands_temp):
        print(f"\nBrand {brand['name']}:")
        parse_brand_phones_and_write_to_excel(url, brand["url"], brand["name"], headers, proxy)


