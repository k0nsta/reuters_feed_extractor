import re
import logging
from time import mktime

import feedparser
from lxml import etree
from urllib import request
from datetime import datetime
from collections import namedtuple
from typing import Set, NamedTuple


ResultSet = Set[NamedTuple]
log = logging.getLogger(__name__)


class ReutersRSSParser:

    def __init__(self, url):
        self.target = url

    def parse(self) -> ResultSet:
        Record = namedtuple('Record', ['url', 'title', 'description', 'content', 'datetime'])
        result = set()

        feed = feedparser.parse(self.target)
        if feed.bozo:
            log.warning("FEED ", feed.bozo)
            err = feed.get('bozo_exception')
            log.error("Socket error : %s", err)
            raise err

        for entry in feed.entries:
            rec = Record(
                url=entry.feedburner_origlink,
                title= entry.title,
                description=re.sub(r'<.*?>', '', entry.summary).strip(),
                content=self._parser_content(entry.feedburner_origlink),
                datetime=datetime.fromtimestamp(mktime(entry.published_parsed))
            )
            result.add(rec)
        log.info('Feed downloaded successfully!')
        return result

    def _parser_content(self, url: str) -> str: 
        raw_data = None
        with request.urlopen(url) as source:
            raw_data = source.read()
        
        parser = etree.HTMLParser() 
        root = etree.fromstring(raw_data, parser)
        content = root.cssselect('.StandardArticleBody_body')
        data = []
        for tag in content:
            for i in tag:
                if i.text:
                    data.append(i.text)
        return ''.join(data)

