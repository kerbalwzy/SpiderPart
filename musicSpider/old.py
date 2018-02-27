# -*- coding:utf-8 -*-
# python version= python3.X
# code lines count about

import re
import requests
from lxml import etree
from customTools.disguiser import user_agent


class CloudMusicSpider(object):
    def __init__(self):
        self.start_url = "http://music.163.com/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset=0"
        self.headers = {"User-Agent":user_agent()}
        # self.detail_part_url = "http://music.163.com"


    def run(self):
        # # create song sheet list page urls and put to queue
        self.create_list_page_urls()
        # # get html string and element than put to queue
        self.get_html_str_and_element()
        # # save the html string as a html file on local
        self.save_list_html_page_local()
        # # get song sheet detail page url and put to queue
        self.get_song_sheet_detail_url()
        # # get song sheet detail element and put to queue
        self.get_song_sheet_str_and_element()
        # # save the html string as a hitm file on local
        self.save_detail_html_page_local()
        # # get song sheet detail info from the detail element
        self.get_song_sheet_detail_info()
        # # save the data into MongoDB
        self.save_songSheet_info_into_MongoDB()

    def create_list_page_urls(self):
        for i in range(38):
            url = self.start_url.format(35 * i)
            # print(url)
            self.list_urls_queue.put(url)
        print("create list page urls success")

    def get_html_str_and_element(self):
        url = self.list_urls_queue.get()
        response = requests.get(url, headers=self.headers)
        # html_str = response.content.decode()
        html_data = response.content
        # '<a href="javascript:void(0)" class="zpgi js-selected">1</a>'
        # list_html_element = etree.HTML(html_str)
        list_html_element = etree.HTML(html_data)
        # print(element)
        page_now = list_html_element.xpath('.//a[@class="zpgi js-selected"]/text()')[0]
        document = {"page_now": page_now, "html_data": html_data}
        self.list_document_queue.put(document)
        self.list_element_queue.put(list_html_element)
        self.list_urls_queue.task_done()
        print("get list page element and document form {} success".format(id(response)))

    def save_list_html_page_local(self):
        document = self.list_document_queue.get()
        with open("./cloudMusic_songSheet/playlistpages/playList_page_{}.html".format(document["page_now"]), "wb") as f:
            f.write(document["html_data"])
        self.list_document_queue.task_done()
        print("save document {} to local success".format(id(document)))

    def get_song_sheet_detail_url(self):
        list_element = self.list_element_queue.get()
        # # <a title="什么秘方才能变成可爱的女孩子呀" href="/playlist?id=957524639" class="msk"></a>
        detail_urls = list_element.xpath('.//a[@class="msk"]/@href')
        # # print([self.detail_part_url + i for i in detail_urls])
        detail_url_list = [self.detail_part_url + url for url in detail_urls]
        for detail_url in detail_url_list:
            self.detail_urls_queue.put(detail_url)
        print("get detail urls from element {} success".format(id(list_element)))


    def get_song_sheet_str_and_element(self):
        detail_url = self.detail_urls_queue.get()
        response = requests.get(url=detail_url, headers=self.headers)
        html_str = response.content.decode()
        element = etree.HTML(html_str)
        request_url = requests.utils.unquote(response.request.url)
        # print(request_url)
        # http://music.163.com/playlist?id=2008788581
        title = re.findall(r"id=(\d*)", request_url)[0]
        document = {"title": title, "text": html_str}
        self.detail_document_queue.put(document)
        self.detail_element_queue.put(element)
        self.detail_urls_queue.task_done()
        print("get detail page element and document from {} success".format(title))

    def save_detail_html_page_local(self):
        document = self.detail_document_queue.get()
        title = document["title"]
        with open("./cloudMusic_songSheet/songsheetpags/songSheetId_{}.html".format(title), "w", encoding="utf-8") as f:
            f.write(document["text"])
        self.detail_document_queue.task_done()
        print("save detail page {} document success".format(title))

    def get_song_sheet_detail_info(self):
        element = self.detail_element_queue.get()
        sheet_id = element.xpath('//div[@id="content-operation"]/@data-rid')[0]
        sheet_url = "http://music.163.com/playlist?id={}".format(sheet_id)
        sheet_title = element.xpath('//h2[@class="f-ff2 f-brk"]/text()')[0]
        sheet_img = element.xpath('//img[@class="j-img"]/@src')[0]
        author_name = element.xpath('//span[@class="name"]//text()')[1]
        create_time = element.xpath('//span[@class="time s-fc4"]/text()')[0][0:10]
        collected_count = element.xpath('//a[@class="u-btni u-btni-fav "]/i/text()')[0][1:-1]
        share_count = element.xpath('//a[@class="u-btni u-btni-share "]/i/text()')[0][1:-1]
        comment_count = element.xpath('//span[@id="cnt_comment_count"]/text()')[0]
        tags = element.xpath('//div[@class="tags f-cb"]//i//text()')
        introduce_temp = element.xpath('//p[@id="album-desc-more"]//text()')[1:-2]
        introduce = "".join(introduce_temp)
        song_count = element.xpath('//span[@id="playlist-track-count"]/text()')[0]
        play_count = element.xpath('//strong[@id="play-count"]/text()')[0]
        info_dict = dict(sheet_id=sheet_id, url=sheet_url, title=sheet_title, img=sheet_img, author=author_name,
                         create_time=create_time, collected_count=collected_count, tags=tags, introduce=introduce,
                         song_count=song_count, play_count=play_count, share_count=share_count,
                         comment_count=comment_count)
        # print(info_dict)
        li_list = element.xpath('//div[@id="song-list-pre-cache"]/ul//li')
        print(len(li_list))
        music_list = []
        for li in li_list:
            music_name = li.xpath('.//a/text()')[0]
            music_url = "http://music.163.com{}".format(li.xpath('.//a/@href')[0])
            music_info = dict(name=music_name, url=music_url)
            music_list.append(music_info)
        info_dict["music_list"] = music_list
        # print(info_dict)
        self.song_sheet_info_queue.put(info_dict)
        self.detail_element_queue.task_done()

    def save_songSheet_info_into_MongoDB(self):
        info_dict = self.song_sheet_info_queue.get()
        objectID = myClient.try_insert_one(info_dict)
        print("save {} into mongoDB success".format(objectID))


if __name__ == '__main__':
    myspider = CloudMusicSpider()
    myspider.run()