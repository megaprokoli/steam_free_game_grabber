from abc import ABC
import requests


class WebScraper(ABC):
    def __init__(self, url, html_parser="html.parser", get_html_with_appid=False):
        self.url = url
        self.html_parser = html_parser
        self.html = None
        self.get_html_with_appid = get_html_with_appid

        if not self.get_html_with_appid:
            self._get_html()

    def _get_html(self):
        self.html = requests.get(self.url).content

    def change_url(self, url):
        self.url = url
        self._get_html()
