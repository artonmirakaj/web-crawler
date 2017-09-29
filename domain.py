# create functions for extracting the domain name
# only stick to links that are in the domain
# don't try to crawl other links ex. facebook, twitter, instagram, etc.


from urllib.parse import urlparse



# get domain name (example.com)
def get_domain_name(url):
    try:
        results = get_sub_domain_name(url).split('.')
        return results[-2] + '.' + results[-1]
    except:
        return ''



# get network location/get sub domain name (name.example.com)
def get_sub_domain_name(url):

    try:
        return urlparse(url).netloc
    except:
        return ''
