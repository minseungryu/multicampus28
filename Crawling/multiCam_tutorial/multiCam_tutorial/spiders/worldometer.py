import scrapy


class WorldometerSpider(scrapy.Spider):
    name = "worldometer"
    allowed_domains = ["www.worldometers.info"]
    start_urls = ["https://www.worldometers.info/world-population/population-by-country/"]

    def parse(self, response):
        """
        step 1
        ---------------------------------------------------------------------
        title = response.xpath('//h1/text()').get() #하나만 가져옴
        # 'a'요소를 추출 for each country (여러개 가져옴)
        countries = response.xpath('//tbody/tr/td/a/text()').getall()
        
        yield {
            'title' : title,
            'countries' : countries
        }
        pass
        
        step 2
        ---------------------------------------------------------------------
        countries = response.xpath('//tbody/tr/td/a')
        for country in countries:
            country_name = country.xpath(".//text()").get()
            country_link = country.xpath(".//@href").get()

            yield {
                'country_name' : country_name,
                'country_link' : country_link
            }
        """
            # 다른 페이지로 넘어가려면 URL이 필요 : 절대경로/상대경로(*scrapy에서 추천)

        countries = response.xpath('//tbody/tr/td/a')

        for country in countries:
            country_name = country.xpath('.//text()').get()
            link = country.xpath('.//@href').get()

            # 다른페이지로 넘어가기
            # 절대경로 사용   '/world-population/saint-helena-population/'
            # absolute_url = f'https://www.worldometers.info/{link}'

            # absolute_url = response.urljoin(link)
            # yield scrapy.Request(url = absolute_url) #request with absolute url

            # 상대경로 사용
            yield response.follow(url=link, callback=self.parse_country, meta = {'country': country_name})

    # 이건 그냥 문법
    def parse_country(self, response):
        country = response.request.meta['country']
        # 클래스명으로 지정, 근데 너무 길다
        # rows = response.xpath('(//table[@class="table table-striped table-bordered table-hover table-condensed table-list"])[1]/tbody/tr')
        # 짧게 쓰는 법(특정 단어 포함여부로: class 에 table이란 단어가 있으면 true)
        # (//table[contains(@class, "table")])[1]/tbody/tr

        rows = response.xpath('(//table[contains(@class, "table")])[1]/tbody/tr')
        
        for row in rows:
            year = row.xpath('.//td[1]/text()').get()
            population = row.xpath('.//td[2]/strong/text()').get()

            yield {
                'country' : country,
                'year' : year,
                'population' : population
            }
        
            