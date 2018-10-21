import requests, json, os
from bs4 import BeautifulSoup as bs
# from pyvirtualdisplay import Display
# from selenium import webdriver
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import datetime
class Site:
    def __init__(self, url):
        self.stem = url

    def staticGet(self, session, url):
        #with requests.session() as s:
        retries = Retry(total=5,
                        backoff_factor=0.5,
                        )
        session.proxies = {}
        session.proxies['http'] = 'socks5h://localhost:9050'
        session.proxies['https'] = 'socks5h://localhost:9050'
        session.mount('http://', HTTPAdapter(max_retries=retries))
        req = session.get(url)
        html = req.text
        # header = req.headers
        # status = req.status_code
        soup = bs(html, 'html.parser')
        return session, req, soup

    def staticPost(self, session, url, data):
        #with requests.session() as s:
        session.proxies = {}
        session.proxies['http'] = 'socks5h://localhost:9050'
        session.proxies['https'] = 'socks5h://localhost:9050'
        req = session.post(url, data=data)
        html = req.text
        header = req.headers
        status = req.status_code
        soup = bs(html, 'html.parser')
        return session, req, soup


'''        
    def dynamicReq(self, url, sec):
        display = Display(visible=0)
        display.start()
        driver = webdriver.Chrome()
        driver.get(url)
        if sec != 0:
            driver.implicitly_wait(sec)
'''


# def staticGet(url):
#     with requests.Session() as s:
#         s.proxies = {}
#         s.proxies['http'] = 'socks5h://localhost:9050'
#         s.proxies['https'] = 'socks5h://localhost:9050'
#
#         req = s.get(url)
#         html = req.text
#         header = req.headers
#         status = req.status_code
#         soup = bs(html, 'html.parser')
#
#     return s, req, soup
#
#
# def staticPost(url, data):
#     with requests.Session() as s:
#         s.proxies = {}
#         s.proxies['http'] = 'socks5h://localhost:9050'
#         s.proxies['https'] = 'socks5h://localhost:9050'
#
#         req = s.post(url, data=data)
#         html = req.text
#         header = req.headers
#         status = req.status_code
#         soup = bs(html, 'html.parser')
#
#     return s, soup


def mkjson(data, path, filename):
    tod = datetime.date.today()
    todstr = tod.isoformat()
    new_directory = os.path.join(path, todstr)
    if not os.path.exists(new_directory):
        os.mkdir(new_directory)
    with open(os.path.join(new_directory, todstr + '_' + filename), 'a', encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent="\t")
