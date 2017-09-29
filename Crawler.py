import requests
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning

class Crawler(object):
    '''
    Abstract class for text crawlers
    '''

    def __init__(self, IN_SAMSUNG):
        # Turn this on if run this script in Samsung
        self.IN_SAMSUNG = IN_SAMSUNG
        self.proxies = {
            "http": "http://109.105.1.52:8080",
            "https": "http://109.105.1.52:8080",
        }
        # Cloak as a browser to avoid anti-cralwers
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"}

        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    def _get_response(self, url):
        '''
        Get response from the given url
        Return: `response` A <Response> object
        '''
        
        try:
            if self.IN_SAMSUNG:
                response = requests.get(
                    url, headers=self.headers, proxies=self.proxies, verify=False)
            else:
                response = requests.get(url, headers=self.headers, verify=False)
            return response
        # Pass if SSL3 server certificate verification fails
        except Exception:
            print("SSL Error, passed")

    def _get_soup(self, url):
        '''
        Convert the response into a BeautifulSoup object
        Return: `soup` A BeautifulSoup object
        '''
        response = self._get_response(url)
        try:
            text = response.text    # Contents of the response in Unicode
            soup = BeautifulSoup(text, "lxml")
            return soup
        # Pass if the response has no contents
        except AttributeError:
            pass

    def _get_links(self, url):
        '''
        Get all hyperlinks from the page
        '''
        soup = self._get_soup(url)
        try:
            htmls = soup.find_all('a')  # Get all hyperlinks
            links = []
            for link in htmls:
                links.append(link.get('href'))

            return links
        # Pass if no links found
        except Exception:
            pass

    def _get_link_strings(self, url):
        '''
        Given a url, get the string of all links if exists
        Return: `link_strings`: A list containing strings of all links
        '''
        soup = self._get_soup(url)
        try:
            htmls = soup.find_all('a')
        # Pass if not contains any links
        except AttributeError:
            return

        link_strings = []
        for link in htmls:
            string = link.string
            if string:    # Avoid empty strings
                link_strings.append(string)

        return link_strings

    def read_lines(self, file_path):
        '''
        Read txt file lines into list
        '''
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        return lines