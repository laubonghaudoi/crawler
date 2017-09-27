'''
# Crawl company names from http://shop.99114.com, start from the category list
Note that the output is not cleaned thus requires preprocessing before 
constructed into data sets.
'''
from Crawler import Crawler


class Crawler_orgs(Crawler):
    '''
    ## A crawler for crawling organization names and infos
    ### Methods:
        - `crawl_org_codes`: Get the codes of organizations for further usage
        - `crawl_orgs_names`: Crawl organization names from [shop.99114.com](shop.99114.com)
        - `crawl_orgs_postals`: Crawl organization postal addresses from the main pages
        - `crawl_orgs_infos`: Crawl organization infos from the info pages
    '''

    def __init__(self, IN_SAMSUNG):
        '''
        ## Crawl organization names from [shop.99114.com](shop.99114.com)
        '''
        super().__init__(IN_SAMSUNG)

        self.orgs_url = "http://shop.99114.com/"

    def _get_area_first_pages(self):
        '''
        Return the link of the first page of organization indices, respresenting that area
        '''
        # We first get all links from the area index page
        areas_page_links = super()._get_links(self.orgs_url)
        # Then find the valid area indices that point to company pages
        area_first_pages = []
        for sublink in areas_page_links:
            # Identify if it is a area index
            if sublink[:32] == 'http://shop.99114.com/list/area/':
                area_first_pages.append(sublink)

        return area_first_pages

    def _get_all_pages(self):
        '''
        Return a list of all pages like 'http://shop.99114.com/list/area/XXXXXX_X'
        '''
        print("Getting the first pages...")
        area_first_pages = self._get_area_first_pages()

        print("Getting all pages...")
        all_urls = []
        for first_page in area_first_pages:
            head = first_page[:-1].replace("http://shop.99114.com", "")
            links = self._get_links(first_page)
            try:
                num_pages = int(links[-2].replace(head, ""))

                for page in range(num_pages):
                    link = first_page.replace("_1", "_" + str(page))
                    all_urls.append(link)
            except:
                pass
        return all_urls

    def _get_org_codes(self, page_urls):
        '''
        Get organization codes
        ### Args:
            `page_urls`: A list of urls like 'http://shop.99114.com/list/area/XXXXXX_X'
        ### Return:
            `org_codes`: A list of organization codes
        '''
        print("Getting organization codes in areas...")
        org_codes = []  # Every element is a list of organizaion links in a page
        for page in page_urls:
            page_links = self._get_links(page)
            for link in page_links:
                if len(link) == 9:
                    link.replace("/", "")
                    org_codes.append(link)

        return org_codes

    def crawl_org_codes(self, page_urls, output_path):
        '''
        Get the codes of organizations given the area index pages
        ### Args:
            `page_urls`: A list of urls like 'http://shop.99114.com/list/area/XXXXXX_X'
            `output_path`: Path for output .txt file
        '''
        print("Crawling organization codes...")
        with open(output_path, 'w', encoding='utf-8') as file:
            for page in page_urls:
                page_links = self._get_links(page)
                for link in page_links:
                    if len(link) == 9:
                        link.replace("/", "")
                        file.writelines(link)
                        file.writelines('\n')

    def crawl_orgs_names(self, page_urls, output_path):
        '''
        Crawl names of organizations from the given pages
        ## Agrs:
            `page_urls`: A list of urls like 'http://shop.99114.com/list/area/XXXXXX_X'
            `output_path`: A file path to output names
        '''
        print("Crawling organization names...")
        all_strings = []
        for page_link in page_urls:
            # Get the strings in this page, in a list of strings
            page_strings = super()._get_link_strings(page_link)
            if page_strings:  # Avoid empty strings
                all_strings.append(page_strings)
            else:
                continue

        print("Crawling completed, writing into file...")
        with open(output_path, 'w+', encoding='utf-8') as output_file:
            for page in all_strings:
                for name in page:
                    if len(name) > 2:
                        output_file.writelines(name)
                        output_file.writelines('\n')

        output_file.close()

    def crawl_orgs_postals(self, codes, output_path):
        '''
        Crawl the address of organizations from its main page
        ### Args:
            `home_urls`: A url like 'http://shop.99114.com/XXXXXXXX'
            `output_path`: Path for output .txt file
        '''
        print('Getting addresses into {}...'.format(output_path))
        with open(output_path, 'w+', encoding='utf-8') as output_file:
            for i, code in enumerate(codes):
                if i % 10000 == 0:
                    print("Crawling code {}".format(i))

                org_page = "http://shop.99114.com/" + code
                soup = self._get_soup(org_page)

                try:
                    addr = soup.find_all(id='detialAddr')
                except AttributeError:
                    print("AtttributeError")
                    continue

                if addr is not None:
                    try:
                        output_file.writelines(addr[0])        
                    except Exception:
                        print("Fuck ! An empty string ??")
                        continue

    def crawl_orgs_infos(self, codes, output_path):
        '''
        Crawl the name, boss, phone information of the organizaion,
        given the the codes
        ### Args:
            `codes`: A list of strings like 'XXXXXXXX'
            `output_path`: Path for output .txt file
        '''
        print("Crawling {}...".format(output_path))
        with open(output_path, 'w+', encoding='utf-8') as output_file:
            for i, code in enumerate(codes):
                if i % 10000 == 0:
                    print("Crawling code {}".format(i))

                org_page = "http://shop.99114.com/" + code + "/ch14"
                try:
                    soup = self._get_soup(org_page)
                    info = soup.title.text
                except:
                    print("Fuck !")
                    continue
                output_file.writelines(info)
                output_file.writelines('\n')
