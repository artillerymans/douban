# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem


class DoubanSpiderSpider(scrapy.Spider):
    #爬虫名
    name = 'douban_spider'
    #允许的域名
    allowed_domains = ['movie.douban.com']
    #入口URL
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        li_List = response.xpath('//div[@class="article"]//ol[@class="grid_view"]//li')
        for i_item in li_List:
            itme = DoubanItem()
            itme['serial_number'] = i_item.xpath(".//div[1]//em/text()").extract_first()
            itme['movie_name'] = i_item.xpath('.//div[@class="hd"]//a//span[1]/text()').extract_first()
            itme['describe'] = i_item.xpath('.//div[@class="bd"]//p[2]//span/text()').extract_first()
            itme['star'] = i_item.xpath('.//div[@class="bd"]//div//span[2]/text()').extract_first()
            itme['evaluate'] = i_item.xpath('.//div[@class="star"]//span[4]/text()').extract_first()
            introduce_list = i_item.xpath('//div[@class="bd"]/p[1]/text()').extract()
            for i_introduce in introduce_list:
                content = "".join(i_introduce.split())
                itme["introduce"] = content
            yield itme
        link_list = response.xpath('//div[@class="paginator"]/span[@class="next"]/link/@href').extract()
        if link_list:
            link = link_list[0]
            yield scrapy.Request("https://movie.douban.com/top250" + link, callback=self.parse)


