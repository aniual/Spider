# -*- coding: utf-8 -*-
import scrapy
from bs4 import UnicodeDammit

from dangdang.items import DangdangItem


class DangspiderSpider(scrapy.Spider):
    name = 'dangSpider'
    key = 'python'
    start_urls = 'http://search.dangdang.com/'

    def start_requests(self):
        self.count= 0
        url = DangspiderSpider.start_urls+'?key='+DangspiderSpider.key
        print(url)
        yield scrapy.Request(url=url,callback=self.parse)


    def parse(self, response):
        try:
            dammit = UnicodeDammit(response.body,['utf-8','gbk'])
            data = dammit.unicode_markup
            selector = scrapy.Selector(text=data)
            lis = selector.xpath("//li[@ddt-pit][starts-with(@class,'line')]")
            for li in lis:
                title = li.xpath("./a[position()=1]/@title").extract_first()
                price = li.xpath("./p[@class='price']/span[@class='search_now_price']/text()").extract_first()
                author = li.xpath("./p[@class='search_book_author']/span[position()=1]/a/@title").extract_first()
                date = li.xpath("./p[@class='search_book_author']/span[position()=last()-1]/text()").extract_first()
                publisher = li.xpath("./p[@class='search_book_author']/span[position()=last()]/a/@title").extract_first()
                detail = li.xpath("./p[@class='detail']/text()").extract_first()
                self.count+=1
                ID = str(self.count)
                while len(ID)<8:
                    ID = '0'+ID
                item = DangdangItem()
                item['id'] = ID
                item['title'] = title.strip() if title else ''
                item['price'] = price.strip() if price else ''
                item['author'] = author.strip() if author else ''
                item['date'] = date.strip()[1:] if date else ''
                item['publisher'] = publisher.strip() if publisher else ''
                item['detail'] = detail.strip() if detail else ''
                yield item
            link = selector.xpath("//div[@class='paging']/ul[@name='Fy']/li[@class='next']/a/@href").extract_first()

            if link:
                url = response.urljoin(link)
                yield scrapy.Request(url=url, callback=self.parse)

        except Exception as err:
            print(err)




