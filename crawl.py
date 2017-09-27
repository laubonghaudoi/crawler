import argparse

from Crawler_orgs import Crawler_orgs
from Crawler_identity import Crawler_identity

parser = argparse.ArgumentParser(description='Crawler')

parser.add_argument('-file', type=int, default=1)

args = parser.parse_args()


identity_crawler = Crawler_identity(IN_SAMSUNG=True)

#orgs_crawler = Crawler_orgs(IN_SAMSUNG=True)

# I have crawled all the org codes, so the codes below might be obsolete 
#links = orgs_crawler.read_lines('all_area_pages.txt')
#orgs_crawler.crawl_org_codes(links, 'all_org_codes.txt')

# Read org codes to crawl directly from their main pages
#codes = orgs_crawler.read_lines('./not_first_codes/56.txt')

# Uncomment the following lines to crawl org postals and places
#orgs_crawler.crawl_orgs_postals(codes, 'post56.txt')

# Uncomment the following lines to crawl org infos
#orgs_crawler.crawl_orgs_infos(codes, "info_56.txt")
num = args.file

#identity_crawler.crawl_identity('name_add{}.txt'.format(num), 'com{}.txt'.format(num), 'title{}.txt'.format(num), 10)
identity_crawler.crawl_com('com.txt{}'.format(num), 'title{}.txt'.format(num), 100)