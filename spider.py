# bunch of links in waiting list
# Spider will grab one of those links and then connect to that page
# once connected, it will grab all the html and throw it into link finder


from urllib.request import urlopen
from link_finder import LinkFinder
from general import *



class Spider:

    # class variable, shared among all instances
    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()

    def __init__(self, project_name, base_url, domain_name):

        # set info.
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'

        # create dir, into new methods
        # connect to a page, gather links
        self.boot()
        self.crawl_page('first spider', Spider.base_url)


    # if first spider, create project directory, then create two data files(queue, crawled)
    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        # make files and add them to folder
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)


    # pass in url, connect to page and get links, then adds them to waiting list
    # take url and add to crawled filed
    @staticmethod
    def crawl_page(thread_name, page_url):

        if page_url not in Spider.crawled:
            print(thread_name + ' now crawling ' + page_url)
            print('Queue ' + str(len(Spider.queue)) + ' | Crawled ' + str(len(Spider.crawled)))

            # connect to web page, return set of all links that it found on that web page
            # then we add it to waiting list
            Spider.add_links_to_queue(Spider.gather_links(page_url))

            Spider.queue.remove(page_url) # remove page we just crawled from waiting list
            Spider.crawled.add(page_url) # adding we we crawled to crawled list

            Spider.update_files()


    # connects to site, takes html, converts it string format, passes it onto LinkFinder
    # parses through it, gets set of all links, then returns them for you if you had no issues
    @staticmethod
    def gather_links(page_url):

        html_string = ''

        try:
            response = urlopen(page_url)

            if response.getheader('Content-Type') == 'text/html':
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")

            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_string)

        except:
            print('Error: cannot crawl page')
            return set() # no links
        return finder.page_links()



    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            # make sure url isn't already in waiting/crawled list
            # we don't want to add them again
            if url in Spider.queue:
                continue
            if url in Spider.crawled:
                continue

            # make sure domain name is in url, no matter what page/link we go on
            if Spider.domain_name not in url:
                continue
            Spider.queue.add(url)


    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)







