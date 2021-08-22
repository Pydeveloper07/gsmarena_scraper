import requests
from bs4 import BeautifulSoup

from scraper import BrandsScraper, PhonesUrlScraper, PhoneScraper
from writer import ExcelBrandWriter


def _get_nav_links(soup, main_url):
    links = []
    nav_block = soup.find("div", class_="nav-pages")
    nav_links = nav_block.find_all("a", href=True)
    for link in nav_links:
        links.append(main_url + link["href"])
    return links


def _parse_and_get_phones(main_url, scrape_urls):
    parsed_results = []
    for url in scrape_urls:
        scraper = PhoneScraper(url, main_url)
        soup = scraper.get_soup()
        main_content = soup.find('div', class_="main-review")
        parsed_results.append(scraper.parse_and_get_result(main_content))

    return parsed_results


def parse_brands_and_write_to_excel(main_url, scrape_url):
    scraper = BrandsScraper(scrape_url, main_url)
    soup = scraper.get_soup()
    main_content = soup.find('div', class_="st-text")
    parsed_results = scraper.parse_and_get_result(main_content.table)

    print(f"Number of brands: {len(parsed_results)}")
    writer = ExcelBrandWriter("brands.xlsx", parsed_results)
    writer.write()

    return parsed_results


def parse_brand_phones_and_write_to_excel(main_url, scrape_url, brand_name):
    source = requests.get(scrape_url).text
    temp_soup = BeautifulSoup(source, "lxml")
    nav_links = _get_nav_links(temp_soup, main_url)
    nav_links.append(scrape_url)
    parsed_urls = []
    for nav_link in nav_links:
        scraper = PhonesUrlScraper(nav_link, main_url)
        soup = scraper.get_soup()
        main_content = soup.find('div', class_="makers")
        parsed_urls += scraper.parse_and_get_result(main_content.ul)

    print(f"Number of phones ({brand_name}): {len(parsed_urls)}")

    parsed_results = _parse_and_get_phones(main_url, parsed_urls)

    # writer = ExcelBrandWriter("brands.xlsx", parsed_results)
    # writer.write()

    return parsed_results


if __name__ == "__main__":
    url = "https://www.gsmarena.com/"
    brands_url = "https://www.gsmarena.com/makers.php3"

    brands = parse_brands_and_write_to_excel(url, brands_url)
    for brand in brands:
        parse_brand_phones_and_write_to_excel(url, brand["url"], brand["name"])


