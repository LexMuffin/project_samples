import scrapy
import json
import csv


class AliexpressSpider(scrapy.Spider):
    name = 'aliexpress'
    allowed_domains = ['aliexpress.ru']
    start_urls = ['https://aliexpress.ru/wholesale?catId=0&initiative_id=SB_20201130063644&SearchText=средство+от+прыщей']
    search_add = 'wholesale?catId=0&initiative_id=SB_20201130063644&SearchText=средство+от+прыщей'
    data = []

    def parse(self, response, **kwargs):
        print(1)
        valid_url = response.url + self.search_add
        yield response.follow(valid_url, callback=self.item_parse)

    def item_parse(self, response, **kwargs):
        print(1)
        js_data = self.js_data_extract(response)
        for i in range(0, len(js_data['items']) - 1):
            temp_data = {'store_name': js_data["items"][i]['store']['storeName'],
                         'title': js_data['items'][i]['title'],
                         'price': js_data['items'][i]['price'],
                         'product_detail_url': 'https:' + js_data['items'][i]['productDetailUrl'],
                        }
            self.data.append(temp_data)


        for i in range(2, self.js_page_extract(response) + 1):
            yield response.follow(response + f'&page={i}', callback=self.item_parse)

        with open("data.csv", "w") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(self.data[0].keys())
            for dict_item in self.data:
                csv_writer.writerow(dict_item.values())


    @staticmethod
    def js_data_extract(response):
        script = response.xpath('//script[contains(text(), "window.runParams =")]/text()').get()
        script_1 = script.replace(";\n", '')
        script_2 = script_1[script_1.index('window.runParams = {"'):script_1.index('_result"}')+len('_result"}')]
        script_3 = script_2.replace("window.runParams = ", '')
        return json.loads(script_3)

    @staticmethod
    def js_page_extract(response):
        script = response.xpath('//script[contains(text(), "window.runConfigs = ")]/text()').get()
        script_1 = script[script.index('"maxPage":'):script.index("maxDisplayPage")]
        script_2 = script_1[script_1.index(':'):script_1.index(",")][1:]
        return script_2