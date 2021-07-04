from bs4 import BeautifulSoup
import re
import urllib.request
import urllib.parse
import collections
import sys
import os
from FileDownload import *
import time

class Crawler:
    DIR_PATH = os.path.dirname(os.path.abspath(__file__))
    DIR_PATH_FILES = 'Downloaded_Files'
    CRAWLED_FILES = 'Crawled Urls.txt'

    def __init__(self):
        self.sleep_time = 1
        self.urls_crawled = {}
        self.exclude_content = ['mailto:', 'favicon', '.ico', '.css', '.js',
                                '.jpg', '.jpeg', '.png', '.gif', '#', '?',
                                '.pdf', '.doc', '.JPG', '.svg', ':']
        self._crawl_count = 0
        self._output = False
        self._filename = '{0}\{1}'.format(self.DIR_PATH, self.CRAWLED_FILES)
        self._max_depth = 0

    @property
    def nr(self):
        return self._crawl_count

    def crawl(self, base_url, filename=None, output=False, max_depth=5):
        self._crawl_count = 0
        self._max_depth = max_depth
        self._output = output
        base_url = base_url.strip()
        if base_url[:7] == 'http://' or base_url[:8] == 'https://':
            pass
        else:
            base_url = 'http://{}'.format(base_url)
        if base_url in self.urls_crawled:
            return
        return self.breadth_first_search(base_url)

    def breadth_first_search(self, base_url):
        print(base_url)
        queued_urls = collections.deque()
        depth = 1
        self.urls_crawled[base_url] = 1
        queued_urls.append(base_url)
        queued_urls.append(depth)

        while len(queued_urls):
            if depth > self._max_depth:
                return True
            base_url = queued_urls.popleft()
            depth = queued_urls.popleft()
            html = self.get_html_content(base_url)
            raw_html = self.get_raw_html(base_url)
            if not html:
                continue
            self._crawl_count += 1
            if self._crawl_count > 1000:
                return True
            self.download_file_and_store_url(base_url, raw_html, depth)
            urls = self.get_urls_to_crawl(base_url, html)
            if self._output:
                self._print_output(
                    self._crawl_count, depth)
            depth += 1
            for url in urls:
                if url not in self.urls_crawled:
                    self.urls_crawled[url] = 1
                    queued_urls.append(url)
                    queued_urls.append(depth)
        return True

    def download_file_and_store_url(self, base_url, html, depth):
        raw_html = BeautifulSoup(html, "html.parser")
        page_body=raw_html.body
        p=page_body.text
        for i in page_body.text:
            if ord(i)<65 or ord(i)>122:
                p=p.replace(i,' ')
            if ord(i)>90 and ord(i)<97:
                p=p.replace(i,' ')
        create_data_files(self.DIR_PATH_FILES, base_url, p.encode('utf-8'), self._crawl_count)
        self._write_to_file(base_url, depth)
        raw_html=''
        
    def get_html_content(self, base_url):
        html_content = None
        try:
            html_bytes = urllib.request.urlopen(base_url).read()
            html_string = html_bytes.decode("utf-8")
            html = collections.namedtuple('HTML', ['html', 'soup'])
            return html(html_string, BeautifulSoup(html_string, "html.parser"))
        except:
            return False

    def get_raw_html(self, base_url):
        html_content = None
        try:
            html_bytes = urllib.request.urlopen(base_url).read()
            html_string = html_bytes.decode("utf-8")
            html = collections.namedtuple('HTML', ['html', 'soup'])
            return html_string
        except:
            return False

    def get_urls_to_crawl(self, base_url, html):
        urls_unique = []
        for url in html.soup.find_all('a'):
            href = url.text
            href = href.lower()
            url = url.get('href')
            check_url = 'https://en.wikipedia.org/wiki/'
            check_url =  urllib.parse.urljoin(base_url, url)
            if url and url not in urls_unique and url != base_url and not any(word in url for word in
                                                                              self.exclude_content) and 'https://en.wikipedia.org/wiki/' in check_url.lower():
                urls_unique.append(check_url)
        return urls_unique

    def _write_to_file(self, base_url, depth):
        with open(self._filename, 'a') as textfile:
            output = 'Depth: {0}, Rank: {1}, URL: {2}\n'.format(depth, self._crawl_count, base_url)
            textfile.write(output)

    def _print_output(self, nr, depth):
        print('Files Crawled: {0} , Depth: {1}'.format(nr, depth))

    def main(self):
        self.crawl('https://en.wikipedia.org/wiki/Sport', 'Crawled Urls.txt', output=True)


if __name__ == '__main__':
    Crawler().main()