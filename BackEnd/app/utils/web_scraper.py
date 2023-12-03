from bs4 import BeautifulSoup
import requests
import logging

class WebScraper:
    def __init__(self, url):
        """
        Constructor for the WebScraper class.

        Args:
            url (str): The URL from which content URLs will be scraped.
        """
        self.url = url
        self.shops = []

    def _get_html(self, url):
        """
        Sends a GET request to the class's URL and returns the response as text.

        Returns:
            str: The HTML content of the webpage as text.
            None: If the GET request fails or the response status code is not 200.

        Raises:
            requests.exceptions.RequestException: If an error occurs during the GET request or the response status code is not 200.
        """
        try:
            response = requests.get(url)
            if response.status_code == 200:
                # Retrieve HTML content and return it
                html_text = requests.get(url).content
                return html_text
            else:
                # Raise an exception if the response status code is not 200
                raise requests.exceptions.RequestException(f"Invalid response status code {response.status_code} for {self.url}")
        
        except requests.exceptions.RequestException as e:
            error_message = 'Error occurred: {}'.format(str(e))
            logging.error(msg=error_message)
            raise requests.exceptions.RequestException(f"Error retrieving HTML from {self.url}: {e}")

    def _parse_html(self, html_text: bytes):
        """
        Parses the HTML content of the webpage using BeautifulSoup and returns a soup object.

        Returns:
            bs4.BeautifulSoup: The soup object containing the parsed HTML content of the webpage.
            None: If the HTML content cannot be retrieved or parsed.

        Raises:
            Exception: If an error occurs during HTML retrieval or parsing.
        """
        try:
            if html_text:
                # Parse HTML content and return soup object
                soup = BeautifulSoup(html_text, 'html5lib')
                return soup
            else:
                # Return None if the HTML content cannot be retrieved or parsed
                return None
        except Exception as e:
            error_message = 'Error occurred during HTML parsing: {}'.format(str(e))
            logging.error(msg=error_message)
            raise e

    def _get_address(self, soup: BeautifulSoup):
        """
        Extracts shop names and addresses from the HTML soup and adds them to the shops list.

        Args:
            soup (bs4.BeautifulSoup): The soup object containing the parsed HTML content of the webpage.
        """
        try:
            shops = []
            address = []
            # Extracting address information from the HTML soup
            mainContent = soup.find('main', attrs={'class':'site-main'})
            siteContent = mainContent.find('div', attrs={'class': 'site-content'})
            tgContainer = siteContent.find('div', attrs={'class': 'tg-container'})
            elementorWidgetContainer = tgContainer.find('div', attrs={'class': 'elementor-element elementor-element-684eb1d elementor-posts--thumbnail-top elementor-grid-3 elementor-grid-tablet-2 elementor-grid-mobile-1 elementor-widget elementor-widget-archive-posts'})
            for article in elementorWidgetContainer.findAll('article', attrs={"class": "elementor-post"}):
                for shop in article.findAll('p'):
                    if 'elementor-heading-title' in shop.get('class', []) and shop.text != "":
                        # Extracting shop name
                        shops.append(shop.text)
                    elif shop.text!= "":
                        # Extracting shop address
                        address.append(shop.text)
            for shop, add in zip(shops, address):
                self.shops.append({"shop":shop, "address":add})

        except Exception as e:
            error_message = f"Error occurred during address extraction: {str(e)}"
            logging.error(msg=error_message)
            raise e

                
    
    def _next_page(self, soup: BeautifulSoup):
        """
        Finds and returns the URL of the next page from the HTML soup.

        Args:
            soup (bs4.BeautifulSoup): The soup object containing the parsed HTML content of the webpage.

        Returns:
            str: The URL of the next page.
            None: If there is no next page.
        """
        try:
            mainContent = soup.find('main', attrs={'class':'site-main'})
            siteContent = mainContent.find('div', attrs={'class': 'site-content'})
            tgContainer = siteContent.find('div', attrs={'class': 'tg-container'})
            elementorWidgetContainer = tgContainer.find('div', attrs={'class': 'elementor-element elementor-element-684eb1d elementor-posts--thumbnail-top elementor-grid-3 elementor-grid-tablet-2 elementor-grid-mobile-1 elementor-widget elementor-widget-archive-posts'})
            elementorPagination = elementorWidgetContainer.find("nav", attrs={"class": "elementor-pagination"})
            next_page = elementorPagination.find("a", attrs={"class": "page-numbers"})
            if next_page.text == "Next":
                return next_page.get('href')
        except Exception as e:
            error_message = f"Error occurred during next page extraction: {str(e)}"
            logging.error(msg=error_message)
            raise e

    def scrap_all_pages(self):
        """
        Scrapes all pages of the website and extracts shop names and addresses.

        Returns:
            list: A list of dictionaries, where each dictionary contains the shop name and address.
        """
        try:
            current_url = self.url
            while current_url is not None:
                print(f"Scrapping from {current_url}")
                html_text = self._get_html(current_url)
                print(f"Parsing data from {current_url}")
                soup = self._parse_html(html_text)
                self._get_address(soup)
                current_url = self._next_page(soup)
            return self.shops
        except Exception as e:
            error_message = f"Error occurred during scraping: {str(e)}"
            logging.error(msg=error_message)
            raise e

if __name__ == "__main__":
    x = WebScraper(url="https://zuscoffee.com/category/store/melaka/").scrap_all_pages()
    print(x)
    print(len(x))