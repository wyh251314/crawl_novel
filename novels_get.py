# -*- coding: utf-8 -*
# 主要用于爬取小说网站看小说用
# 主要功能模块：自动获取代理模块，爬取模块，数据处理模块，输出模块


import requests
import time
import urllib3

from proxies_pool import PROXIES
from lxml import etree

# 代理ip
# PROXY = "112.5.56.2:9091"
START_URL = "https://www.yingsx.com/0_381/"
NOVEL_NAME = "临渊行.txt"
# os.environ['NO_PROXY'] = 'https://www.yingsx.com'

urllib3.disable_warnings()

class GetNovel:
    def __init__(self):
        """
            用一个类来完成
        """
        self.headers = {
                        "User-Agent":'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
                        "Accept":'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                        "Host":'www.yingsx.com',
                        'Connection':'close',
                        }
        
        # self.start_url =  "https://www.yingsx.com/57_57094/"
        self.url_pre = "https://www.yingsx.com"
        self.all_url = []
        self.next_url = ""
        self.chapter_num = 20 # 章节数
        self.novel_name = ""
        self.f = open(NOVEL_NAME, "a")
        self.proxies_pool = []

    def get_ips(self):
        pool_lists = PROXIES()
        self.proxies_pool = pool_lists.get_pool()
        if len(self.proxies_pool) == 0:
            print("代理池获取不到ip")

    def crawler(self, url):
        try:
            proxies = {
                            'http:':"http://" + self.proxies_pool[0],
                            'https:' : 'https://' + self.proxies_pool[0],
            }
            resp = requests.get(url, headers=self.headers, proxies=proxies, verify=False)
            resp.encoding="utf-8"
            html = etree.HTML(resp.text)
            return html
        except Exception as ex:
            print("crawler error, error message:", ex)
            return None

    def get_next_url(self, url):
        html = self.crawler(url)
        next_url = html.xpath("""//div[@id='wrapper']/div[@class='content_read']/div[@class='box_con']/div[@class='bookname']/div[@class='bottem1']/a[4]/@href""")
        
        self.all_url.append(self.url_pre + next_url[0].strip())
        self.next_url = self.url_pre + next_url[0].strip()
        # print(self.next_url)
    
    def get_index_url(self,url):
        html = self.crawler(url)
        if html is None:
            return None
        self.novel_name = html.xpath("""//div[@id='wrapper']/div[@class='box_con']/div[@id='maininfo']/div[@id='info']/h1/text()""")
        # all_chapter_name = html.xpath("""//div[@id='wrapper']/div[@class='box_con']/div[@id='list']/dl/dd[position()>9]/a/text()""")
        all_url_tail = html.xpath("""//div[@id='wrapper']/div[@class='box_con']/div[@id='list']/dl/dd[position()>9]/a/@href""")
        for url_tail in all_url_tail:
            url = self.url_pre + url_tail
            # print(url)
            self.all_url.append(url)
        print("novel_name:", self.novel_name)
        self.chapter_num = len(self.all_url) -1
        print("章节数：", self.chapter_num)
            
    def get_notes_content(self, url):
        """
            获取详情页下面所有的小说内容与章节名，并写入到指定文件
        """
        html = self.crawler(url)
        if html is None:
            del self.proxies_pool[0]
            html = self.crawler(url)
            if html is None:
                return None
        # 章节名.是一个list
        chapter = html.xpath("""//div[@id='wrapper']/div[@class='content_read']/div[@class='box_con']/div[@class='bookname']/h1/text()""")
        # 小说内容,list
        result = html.xpath('//div[@id="wrapper"]/div[@class="content_read"]/div[@class="box_con"]/div[@id="content"]/text()')

        chapter = chapter[0].strip()

        if "第" not in chapter:
            return
        print(chapter)
        self.f.write(chapter)
        self.f.write("\n")
        time.sleep(0.1)
        for line in result:
            if line.strip() == "":
                continue
            # print(line)
            self.f.write(line)
        self.f.write("\n")

    def circle_crawler(self, start_url):
        """
            读取当前页信息,然后获取下一页的url,并循环遍历读取
        """
        for i in range(self.chapter_num):
            if self.next_url == "":
                self.crawler(start_url)
            else:
                self.crawler(self.next_url)
            time.sleep(1)
            i+=1

    def simple_crawler(self, url):
        """
            获取目录页下面所有的章节url
        """
        self.get_index_url(url)
        if self.all_url:
            for _url in self.all_url:
                self.get_notes_content(_url)
            
    def main(self):
        # 获取可用的代理ip
        self.get_ips()
        # 通过目录页去获取所有章节address来爬取所有网页
        self.simple_crawler(START_URL)
        # 通过第一页（起始页）不断通过下一页去获取所有的章节address
        # self.circle_crawler(START_URL)
        self.f.close()


class TestGetNovel(GetNovel):

    def __init__(self):
        GetNovel.__init__(self)

    def test_get_index_url(self,url):
        html = self.crawler(url)
        if html is None:
            return None
        all_chapter_name = html.xpath("""//div[@id='wrapper']/div[@class='box_con']/div[@id='list']/dl/dd[position()>9]/a/text()""")
        all_url_tail = html.xpath("""//div[@id='wrapper']/div[@class='box_con']/div[@id='list']/dl/dd[position()>9]/a/@href""")
        for url_tail in all_url_tail:
            url = self.url_pre + url_tail
            print(url)
            self.all_url.append(url)
        print(len(self.all_url))
    
    def main(self):
        # html = self.crawler(START_URL)
        # print(html)
        # self.test_get_all_url(START_URL)
        url = "https://www.yingsx.com/36_36953/23979398.html"
        self.get_notes_content(url)

        self.f.close()

getnovel = GetNovel()
# a = TestGetNovel()
getnovel.main()
