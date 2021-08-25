# from bs4 import BeautifulSoup, NavigableString
#
# with open("test.html") as source:
#     soup = BeautifulSoup(source, "lxml")
#
# loudspeaker_row = soup.find_all("tr")[0]
# loudspeaker = loudspeaker_row.find("td", class_="nfo").text
# jack_row = soup.find_all("tr")[1]
# jack = jack_row.find("td", class_="nfo").text
# print(loudspeaker)
# print(jack)
# chipset = chipset.next.next
# print(chipset)

try:
    x = 1/0
except Exception:
    try:
        x = 1/"s"
    except:
        x =1/4


