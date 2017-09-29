# looking at html, sifting through it, find all the links, <a> tags

from html.parser import HTMLParser
from urllib import parse



class LinkFinder(HTMLParser):

    def __init__(self, base_url, page_url):
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.links = set() # crawling links, storing them in here

    # when HTMLParser feed() is called, this function is called when it encounters the tag <a>
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (attribute, value) in attrs:
                if attribute == 'href':
                    url = parse.urljoin(self.base_url, value)
                    self.links.add(url)


    def page_links(self):
        return self.links

    def error(self, message):
        pass