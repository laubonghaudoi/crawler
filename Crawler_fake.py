from Crawler import Crawler

class Crawler_fake(Crawler):
    '''
    Crawl generated English info
    '''
    def __init__(self, IN_SAMSUNG):
        super().__init__(IN_SAMSUNG)

        self.fake_url = "http://www.fakenamegenerator.com/"
        self.com_url = "http://www.fakepersongenerator.com/employment-generator"

    def crawl_fake(self, name_address_path, company_path, title_path, num):
        name_address_file = open(name_address_path, 'w', encoding='utf-8')
        company_file = open(company_path, 'w', encoding='utf-8')
        title_file = open(title_path, 'w', encoding='utf-8')

        for i in range(num):
            if i % 1000 == 0:
                print("Crawling generated fake identites {}".format(i))
            soup = self._get_soup(self.fake_url)
            
            try:
                dd = soup.find_all('dd')
            except TypeError:
                continue
            
            name_address = str(soup.find_all(class_='address'))
            name_address_file.writelines(name_address +'\n')          

            company = str(dd[16])
            company_file.writelines(company.replace('</dd>', '\n'))

            title = str(dd[17])
            title_file.writelines(title.replace('</dd>', '\n'))

        name_address_file.close()
        company_file.close()
        title_file.close()

    def crawl_com(self, com_path, title_path, num):
        com_file = open(com_path, 'w', encoding='utf-8')
        title_file = open(title_path, 'w', encoding='utf-8')

        for i in range(num):
            if i % 1000 == 0:
                print("Crawling generated fake company {}".format(i))

            soup = self._get_soup(self.com_url)

            try:
                info = soup.find_all(class_="info-detail")
            except Exception:
                continue
            
            title = str(info[3]) + '\n'
            com = str(info[4]) + '\n'

            title_file.writelines(title)
            com_file.writelines(com)

        title_file.close()
        com_file.close()