from bs4 import BeautifulSoup
import re

from scraper.web_scraper import WebScraper


class GameScraper(WebScraper):
    def __init__(self, url, html_parser="html.parser"):
        """
        Used to scrape a Steam game store page and get the appid if the games is free.
        :param url:
        :param html_parser:
        """
        super().__init__(url, html_parser)
        self._re_game_area = re.compile("game_area_purchase_game free_weekend")
        self._re_appid = re.compile(r"[0-9]{5,}")

    def __extract_appid(self):
        appid = self._re_appid.search(self.url)

        if appid:
            return appid.group()

    def get_appid(self):
        soup = BeautifulSoup(self.html, self.html_parser)
        buy_area = soup.find("div", attrs={"class": self._re_game_area})

        if buy_area:
            return self.__extract_appid()
