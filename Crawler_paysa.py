from Crawler import Crawler

class Crawler_paysa(Crawler):
    '''
    Crawl company names and job titles from https://www.paysa.com
    '''
    def __init__(self, IN_SAMSUNG):
        super().__init__(IN_SAMSUNG)

        self.company_url = "https://www.paysa.com/jobs/directory/company?page="
        self.title_url = "https://www.paysa.com/jobs/directory/title?page="
    
    def crawl_company(self, output_path):
        output_file = open(output_path, 'w', encoding='utf-8')
        
        for i in range(5, 914):
            soup = self._get_soup(self.company_url + str(i))

            company = soup.find_all(class_="torso-listing-entry")

            output_file.writelines(str(company))
        
        output_file.close()
    
    def crawl_title(self, output_path):
        output_file = open(output_path, 'w', encoding='utf-8')
        
        for i in range(5, 517):
            soup = self._get_soup(self.title_url + str(i))

            title = soup.find_all(class_="torso-listing-entry")

            output_file.writelines(str(title))
        
        output_file.close()