dynamic_links
=============
Scrapy spider to crawl and extract dynamic links from specific domains

To run: 
	scrapy crawl dynamic_links -a target=homepage
	for example:
		scrapy crawl dynamic_links -a target=http://www.mit.edu/

	the output file will be saved into output/

some useful settings: placed in dynamic_links/settings.py
	DOWNLOAD_DELAY = 0.1
	DEPTH_LIMIT = 20

	You can change them as you want.