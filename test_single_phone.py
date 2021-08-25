from scraper import PhoneScraper
from writer import ExcelPhoneWriter


def scrape():
    headers = {
        "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    }
    proxy = {
        "https": "34.146.31.30:3128"
    }
    url = "https://www.gsmarena.com/zte_axon_30_5g-11020.php"
    main_url = "https://www.gsmarena.com/"
    scraper = PhoneScraper(url, main_url)
    soup = scraper.get_soup(headers, proxy)
    main_content = soup.find('div', class_="main-review")
    parsed_result = scraper.parse_and_get_result(main_content)
    writer = ExcelPhoneWriter("test.xlsx", [parsed_result])
    writer.write()


if __name__ == "__main__":
    scrape()