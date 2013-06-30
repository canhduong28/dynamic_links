#encoding=utf-8
import re
import os
import time
from scrapy import log
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.http import Request
from urlparse import urljoin, urlparse

from dynamic_links.items import Link

class Spider(BaseSpider):
    name = 'dynamic_links'
    target = None
    dynamic_patterns = [
                        r'\.php\?.+',
                        r'\.asp\?.+',
                        r'\.aspx\?.+',
                    ]

    def __init__(self, target='http://www.mit.edu/'):
        self.target = target
        self.domain = urlparse(target).netloc
        pattern = re.sub(r'\.', '\.', urlparse(target).netloc)
        if 'www' in pattern:
            pattern = re.sub(r'www\\.', r'[a-z0-9]*\.?', pattern)
        else:
            pattern = r'[a-z0-9]*\.?' + pattern
        print pattern
        #pattern = r'' + pattern
        self.pattern = pattern

        # create output file
        filename = re.sub(r'\.', '-', self.domain)
        filename = 'output/' + filename + '.txt'
        with open(filename, 'w') as f:
            f.close()
        self.output = os.path.abspath(filename)
        
        pass

    def start_requests(self):
        if self.domain == 'tudelft.nl' or self.domain == 'www.tudelft.nl':
            self.target = 'http://cookie.tudelft.nl/index.php?choice-button=yes&use-cookies=yes&lang=nl&action=ask&origin=http%3A%2F%2Fwww.tudelft.nl%2F%2F'
            req = Request(self.target, dont_filter=False, callback=self._parser)
            req.meta['orig_url'] = self.target
            req.headers['choice-button'] = 'yes'
            req.headers['use-cookies'] = 'yes'
            req.headers['action'] = 'ask'
        else:
            req = Request(self.target, dont_filter=False, callback=self._parser)
            req.meta['orig_url'] = self.target
        yield req

    def _parser(self, response):
        orig_url = response.request.meta['orig_url']

        try:
            hxs = HtmlXPathSelector(response)
            log.msg('[CRAWLED] %s' % response.url, level=log.INFO)
            href_list = set(hxs.select('//a/@href').extract())
            for href in href_list:
                href = urljoin(orig_url, href)
                
                if href[:4] != 'http':
                    continue
                

                domain = urlparse(href).netloc
                
                if re.search(self.pattern, domain):

                    req = Request(href, dont_filter=False, callback=self._parser)
                    req.meta['orig_url'] = href
                    #req.meta['root'] = False

                    yield req
                    #print href

                    for p in self.dynamic_patterns:
                        if re.search(p, href):
                            item = Link()
                            item['url'] = href
                            yield item

        except:
            pass
        




            