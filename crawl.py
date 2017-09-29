import argparse

from Crawler_orgs import Crawler_orgs
from Crawler_fake import Crawler_fake
from Crawler_paysa import Crawler_paysa
'''
parser = argparse.ArgumentParser(description='Crawler')
parser.add_argument('-file', type=int, default=1)

args = parser.parse_args()


#orgs_crawler = Crawler_orgs(IN_SAMSUNG=True)

# I have crawled all the org codes, so you don't have to run the codes below again 
links = orgs_crawler.read_lines('all_area_pages.txt')
orgs_crawler.crawl_org_codes(links, 'all_org_codes.txt')

# Read org codes to crawl directly from their main pages, file name should be changed
codes = orgs_crawler.read_lines('./not_first_codes/56.txt')

# Crawl org postals and places from the c
orgs_crawler.crawl_orgs_postals(codes, 'post56.txt')

# Uncomment the following lines to crawl org infos
orgs_crawler.crawl_orgs_infos(codes, "info_56.txt")

num = args.file
'''
c = Crawler_paysa(True)
c.crawl_company('paysacom.txt')
c.crawl_title('paysatitle.txt')