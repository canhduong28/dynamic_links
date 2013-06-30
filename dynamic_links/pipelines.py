from scrapy import log
import os
import re
from dynamic_links.settings import *
from dynamic_links.items import Link
from scrapy import signals
from scrapy.exceptions import DropItem

class StorePipeline(object):
    def __init__(self):
        self.dynamic_patterns = set()

    def get_pattern(self, link):
        return re.sub(r'=.+', '=*', link)

    def process_item(self, item, spider):
        pattern = self.get_pattern(item['url'])

        if pattern in self.dynamic_patterns:
            #raise DropItem("Duplicate item found: %s" % item)
            return
        else:
            self.dynamic_patterns.add(pattern)
            filename = spider.output
            
            with open(filename, 'ab') as f:
                f.write(item['url'] + '\n')
                f.close()
            
            return item