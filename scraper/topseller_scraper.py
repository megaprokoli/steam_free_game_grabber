from bs4 import BeautifulSoup
import re

from scraper.web_scraper import WebScraper


class TopsellerScraper(WebScraper):
    def __init__(self, url, html_parser="html.parser"):
        super().__init__(url, html_parser)

    def get_urls(self):
        soup = BeautifulSoup(self.html, self.html_parser)
        tags = soup.findAll("a", attrs={"class": "tab_item"})
        # print(tags)
        return [(lambda t: t["href"])(t) for t in tags]
