#encoding=utf-8
from flask import Flask
from exts import db
import config
import requests
from bs4 import BeautifulSoup
from models import Idiom
app = Flask(__name__)
db.init_app(app)
app.config.from_object(config)
@app.route('/')
def hello_world():
    return 'Hello World mum!'

@app.route('/init',methods=['GET'])
def write_idiom_to_db():
    # 初始化成语数据到DB
    # 爬取首字字母索引（A，B，C,D....）
    url = 'http://chengyu.teachercn.com'
    soup_index = getSoup(url)
    index_menu = soup_index.find_all('menu', {'class': 'bs_index4'})[1]
    index_links = index_menu.find_all('a')
    for index_link in index_links:
        Initials = index_link['title']
        soup = getSoup(url + index_link['href'])
        idiom_index = soup.find('menu', {'class': 'py_index3'})
        index_list = idiom_index.find_all('a')
        for index in index_list:
            soup_idiom = getSoup(url + index['href'])
            idiom_menu = soup_idiom.find('menu', {'class': 'bs_index7'})
            idioms = idiom_menu.find_all('a')
            for idiom in idioms:
                soup_idiom_details = getSoup(url + idiom['href'])
                details_div = soup_idiom_details.find_all('div', {'class': 'notice'})
                details = ''
                for i in range(len(details_div)):
                    if i not in (0, 1, 6, len(details_div) - 1, len(details_div) - 2):
                        if i < 5:
                            details = details + details_div[i].text.split(',')[0]
                        else:
                            details = details + details_div[i].text
                        details = details + '|'
                Pinyin = details_div[0].text.split('(')[1].split(')')[0]
                FirstPinyin = idiom['href'].split('/')[1]
                idiom_data = Idiom(Initials=Initials, FirstPinyin=FirstPinyin, idiom=idiom.text,Pinyin=Pinyin,details=details)
                db.session.add(idiom_data)
                db.session.commit()
                # idiom=idiom.text
                #writer.writerow((idiom['href'].split('/')[1], idiom.text))def getSoup(url):

def getSoup(url):
    '''
        公共方法根据传入的url获取soup
    '''
    r = requests.get(url, timeout=30)
    r.encoding = 'gbk'
    # print (r.text)
    soup = BeautifulSoup(r.text, 'lxml')
    return soup

if __name__ == '__main__':
    app.run()
