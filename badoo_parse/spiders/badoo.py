import scrapy
import json


class BadooSpider(scrapy.Spider):
    name = 'badoo'
    allowed_domains = ['badoo.com']
    start_urls = ['https://badoo.com/']
    login_url = 'https://badoo.com/webapi.phtml?SERVER_LOGIN_BY_PASSWORD'

    def __init__(self, login, password, *args, **kwargs):
        self.login = login
        self.password = password
        super().__init__(*args, **kwargs)

    def parse(self, response, **kwargs):
        #try:
            js_data = self.js_data_extract(response)
            yield scrapy.FormRequest(
                self.login_url,
                method='POST',
                callback=self.parse,
                formdata={
                    'user': self.login,
                    'password': self.password,
                    'remember_me': 'true',
                },
                    headers={'X-Session-id': js_data['Apification']['session_id']},
            )
        #except AttributeError as e:
        #    yield response.follow(f'dating/united-states/', callback=self.after_login)

    def after_login(self, response):
        print(1)

    @staticmethod
    def js_data_extract(response):
        script = response.xpath('//script[contains(text(), "$vars=")]/text()').get()
        return json.loads(script.replace("$vars=", '')[1:-2])