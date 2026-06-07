import requests
from bs4 import BeautifulSoup
from utils import clean_text, save_json

class WebScraper:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0"
        })

    def fetch(self, url: str) -> BeautifulSoup:
        response = self.session.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")

    def extract(self, soup: BeautifulSoup) -> list:
        results = []
        for item in soup.select("article, .item, li"):
            text = clean_text(item.get_text())
            if text:
                results.append({"text": text})
        return results

    def run(self, output: str = "output.json"):
        soup = self.fetch(self.base_url)
        data = self.extract(soup)
        save_json(data, output)
        print(f"Saved {len(data)} items to {output}")
