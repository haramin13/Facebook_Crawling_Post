# Facebook_Crawling_Post

##About this tool
A tool for scraped posts from pages on facebook
This tool was write base on **facebook-scraper-selenium** of author **apurvmishra99**
You can find source code [in here](https://github.com/apurvmishra99/facebook-scraper-selenium).

##To run tool
usage: facebook_crawl_post/fblogin.py [-h] [--pages PAGES [PAGES ...]] [-d DEPTH]
Data Collection
arguments:
  -h, --help            show this help message and exit
  -p, --pages PAGES [PAGES ...]
                        List the pages you want to scrape
                        for recent posts
  
  -d DEPTH, --depth DEPTH
                        How many recent posts you want to gather in
                        multiples of (roughly) 8.
                        
Finnaly, you can running facebook_crawl_post/check_duplicate.py to find out the duplicate posts ware scraped
