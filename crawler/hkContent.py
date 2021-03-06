import requests, json, os
from bs4 import BeautifulSoup as bs
import Crawler as cr
import time
from multiprocessing import Pool
from itertools import repeat
from collections import OrderedDict
import re
import datetime
import hkTitleCrawl as hktc


def getContent(session, object, title):
    error_data = OrderedDict()
    return_data = OrderedDict()

    highkorea = object
    s = session
    topicurl = title['titleURL']
    topictitle = title['title']
    topicauthor = title['author']
    lastup = title['lastup']
    try:
        tup = highkorea.staticGet(s, highkorea.stem + topicurl.strip('.'))
        s, html, soup = tup[0], tup[1].text, tup[2]
        lastpg = soup.select('div.topic-actions div span a')
        lastpage = lastpg[-1].get('href') if lastpg != [] else soup.select('#page-body h2 a')[0].get('href')
        m = re.compile('&start=(\d+)').search(lastpage)
        num = 1
        if m:
            num = int(m.group(1))
            url = re.sub('&start=(\d+)', '', lastpage)
        else:
            url = lastpage
        content_datas=list()
        html_datas=list()
        image_datas = list()
        for i in range(0, num, 10):
            tup = highkorea.staticGet(s, highkorea.stem + url.strip('.') + '&start={}'.format(i))
            s, html, soup = tup[0], tup[1].text, tup[2]
            authors = soup.select(".author strong a.username-coloured")
            contents = soup.find_all('div', {'class':'content'})
            images = soup.select('dl.attachbox dd dl dt a img')
            for author, content in zip(authors, contents):
                content_data=OrderedDict()
                for br in content.find_all('br'):
                    br.replace_with('\n')
                content_data['author']=author.text
                content_data['content']=content.text
                content_datas.append(content_data)
            for image in images:
                image_data = OrderedDict()
                image_data['src'] = image.get('src')
                image_data['name'] = image.get('alt')
                image_datas.append(image_data)
            html_datas.append(html)
        return_data['image'] = image_datas
        return_data['html'] = html_datas
        return_data['content'] = content_datas
        return_data['url'] = topicurl
        return_data['title'] = topictitle
        return_data['author'] = topicauthor
        return_data['lastup'] = lastup
        # return_data[topicurl] = return_data
        return return_data
    except Exception as e:
        error_data[title['titleURL']] = e
        cr.mkjson(error_data, '/home/kyw/json_datas/highkorea', 'hkContent_error.json')
        pass
if __name__=='__main__':
    tod = datetime.date.today()
    todstr = tod.isoformat()
    loginPage = 'http:Char//highkorea5ou4wcy.onion/ucp.php?mode=login'
    mainpage = 'http://highkorea5ou4wcy.onion'
    ID = 'michin'
    passwd = 'michin'
    LOGIN_INFO = {
        'username': ID,
        'password': passwd
    }
    start_time = time.time()

    highkorea = cr.Site(mainpage)
    session = hktc.highkorealogin(LOGIN_INFO, highkorea, loginPage)[0]
    directory = os.path.join('/home/kyw/json_datas/highkorea/', todstr)
    filepath = os.path.join(directory, todstr + '_' + 'hkTitle.json')
    with open(filepath) as f:
        data = json.loads(f.read(), encoding ="utf-8")
        for i, forum in enumerate(data):
            content = list()
            pool = Pool(processes=4)  # 4개의 프로세스를 사용합니다.
            results = pool.starmap(getContent, zip(repeat(session), repeat(highkorea), forum))
            cr.mkjson(results, '/home/kyw/json_datas/highkorea','{}_hkContent.json'.format(i))#2018-10-21_1_hkContent.json
