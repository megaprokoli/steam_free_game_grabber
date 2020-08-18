from bs4 import BeautifulSoup
import requests
import re

from scraper.web_scraper import WebScraper


class NewsScraper(WebScraper):
    def __init__(self, url, filter_terms, html_parser="html.parser"):
        """
        Used to scrape Steam newsfeeds and get appids of free games.
        :param url:
        :param filter_terms:
        :param html_parser:
        """
        super().__init__(url, html_parser)

        self.filter_terms = filter_terms
        self._re_post_id = re.compile(r"[0-9]{9,}")
        self._re_appid = re.compile(r"[0-9]{5,}")
        self._re_free = re.compile("|".join(self.filter_terms))

    def extract_post_ids(self):
        soup = BeautifulSoup(self.html, self.html_parser)
        posts = [str(a) for a in soup.findAll("a", attrs={"href": "#"})]
        posts = filter(lambda p: self._re_free.findall(p), posts)
        ids = []

        for p in posts:
            match = self._re_post_id.search(p)

            if match:
                ids.append(match.group())
        return ids

    def extract_appids(self, post_ids: list):
        appids = set()

        for pid in post_ids:
            full_post = requests.get("https://store.steampowered.com//news/post/" + pid).content
            soup = BeautifulSoup(full_post, self.html_parser)

            games = [str(a) for a in soup.find_all("a",
                                                   attrs={"href": re.compile(r"http://store.steampowered.com/app/[^>]+")})]

            for g in games:
                match = self._re_appid.search(g)

                if match:
                    appids.add(match.group())
        return appids
