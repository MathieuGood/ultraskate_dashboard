from bs4 import BeautifulSoup
from webscraper.browser_manager import BrowserManager


class Webscraper:
    """
    A class that provides methods for web scraping and extracting information from web pages.
    """

    @classmethod
    def fetch_html(cls, url: str) -> BeautifulSoup:
        """
        Fetches the HTML content from the specified URL.

        :param url: The URL to fetch the HTML content from.
        :return: The BeautifulSoup object representing the parsed HTML content.
        """
        page = BrowserManager.new_page()
        page.goto(url, timeout=60_000, wait_until="domcontentloaded")
        page.wait_for_load_state("domcontentloaded")
        html = page.content()
        page.close()

        soup = BeautifulSoup(html, "html.parser")

        title_tag = soup.title
        if title_tag and title_tag.get_text(strip=True) == "Just a moment...":
            print("Encountered Cloudflare protection page : page not scraped.")
        return soup
