import requests
from .web_scraper import WebScraper
import re
import json
import logging

class LocationScraper:
    def __init__(self, url) -> None:
        """
        Initialize the LocationScraper with the given URL.

        Args:
            url (str): The URL to scrape.

        Attributes:
            url (str): Store the URL.
            shops (list): A list of shops scraped from the URL.
            jalan_pattern (re.Pattern): Compiled regex pattern to find 'jalan' in addresses.
            postal_code_pattern (re.Pattern): Compiled regex pattern to find postal codes.
        """
        self.url = url
        self.shops = WebScraper(url=self.url).scrap_all_pages()
        self.jalan_pattern = re.compile(r'\b(?:\S+\s+)?jalan\s+(.+)\b|\bjalan\s+(.+)|\b(?:\S+\s+)?jln\s+(.+)\b|\bjln\s+(.+)')
        self.postal_code_pattern = re.compile(r'\b\d{5}\b')

    def _process_location(self, shop):
        """
        Process the location data of a shop.

        Args:
            shop (dict): A dictionary containing shop details.

        Returns:
            dict: A dictionary with processed location details.
        """
        """Split the shop and address information."""
        location = shop["shop"].lower().split(" – ")
        address = shop["address"].lower().split(",")
        output = {"shop": re.sub(r".*?@", "", location[-1]).strip()}

        try:
            for word in address:
                """Extract 'jalan' and postal code from the address."""
                jalan_match = self.jalan_pattern.search(word)
                postal_code_match = self.postal_code_pattern.search(word)
                
                if jalan_match:
                    """Combine the matched 'jalan' groups."""
                    match = f"jalan {jalan_match.group(1) or jalan_match.group(2) or jalan_match.group(3) or jalan_match.group(4)}"
                    output["jalan"] = match
                if postal_code_match:
                    output["postal_code"] = postal_code_match.group(0)

            return output
        
        except Exception as e:
            error_message = f"Error occurred during process location: {str(e)}"
            logging.error(msg=error_message)
            raise e


    def _get_search_params(self, shop):
        """
        Generate search parameters from a shop's location.

        Args:
            shop (dict): A dictionary containing shop details.

        Returns:
            dict: A dictionary of search parameters.
        """
        """Process the location and format for URL query."""
        x = self._process_location(shop)
        return {key: value.replace(" ", "+") for key, value in x.items()}

    def _make_api_request(self, search_params, prefix=None):
        """
        Make an API request to get location data.

        Args:
            search_params (list): A list of search parameters.
            prefix (str, optional): An additional prefix for the search query.

        Returns:
            dict: The API response as a dictionary.
        """
        """Filter out empty parameters and add a prefix."""
        search_params = [item for item in search_params if item != ""]
        search_params.append(prefix)
        search_param = '+'.join(search_params)
        url = (
            "https://nominatim.openstreetmap.org/search?q="
            f"{search_param}&format=json"
        )
        response = requests.get(url)
        return json.loads(response.content)
    
    def scrape_locations(self):
        """
        Scrape locations for all shops.

        Raises:
            Exception: If an error occurs during scraping.
        """
        try:
            for count, shop in enumerate(self.shops, start=1):
                print(f"{count}/{len(self.shops)}", end="\r", flush=True)
                search_params = self._get_search_params(shop)
                
                """Different combinations of search parameters"""
                combinations = [
                    [search_params.get('shop', ''), search_params.get('jalan', ''), search_params.get('postal_code', '')],
                    [search_params.get('shop', ''), search_params.get('postal_code', '')],
                    [search_params.get('jalan', ''), search_params.get('postal_code', '')],
                ]

                for combo in combinations:
                    results = self._make_api_request(combo, prefix="melaka")
                    if results:
                        """Assuming we want to take the first result"""
                        shop["location"] = {"lon": results[0]["lon"], "lat": results[0]["lat"]}
                        break 

        except Exception as e:
            error_message = f"Error occurred during scrapping location: {str(e)}"
            logging.error(msg=error_message)
            raise e

    @property
    def shop_details(self):
        self.scrape_locations()
        return self.shops
    
    @property
    def shop_name(self):
        return [shop["shop"] for shop in self.shops]
    
    @property
    def shop_address(self):
        return [shop["address"] for shop in self.shops]

if __name__ == "__main__":
    x = LocationScraper(url="https://zuscoffee.com/category/store/melaka/").shop_details
    print(x)