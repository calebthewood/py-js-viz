import scrapy


BASE_URL = "https://en.wikipedia.org"
BASE_URL_ESCAPED = 'http:\/\/en.wikipedia.org'

class NWinnerItemBio(scrapy.Item):
    link = scrapy.Field()
    name = scrapy.Field()
    mini_bio = scrapy.Field()
    image_urls = scrapy.Field()
    bio_image = scrapy.Field()
    images = scrapy.Field()

class NWinnerSpiderBio(scrapy.Spider):

    name = 'nwinners_minibio'
    allowed_domains = ['en.wikipedia.org']
    start_urls = [
        "https://en.wikipedia.org/wiki/List_of_Nobel_laureates_by_country"
    ]

    custom_settings = {
        'ITEM_PIPELINES': {'nobel_winners.pipelines.NobelImagesPipeline': 1}
    }

    def parse(self, response):
        # filename = response.url.split('/')[-1]
        h3s = response.xpath('//h3')

        # xpath to p tag containing bio
        #   //*[@id="mw-content-text"]/div[1]/p[2]
        # xpath to image
        #   //*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr[2]/td/span/a/img

        # //table[contains(@class, "biography")]//img/@src

        for h3 in h3s:
            country = h3.xpath('span[@class="mw-headline"]/text()').extract()
            if country:
                winners = h3.xpath('following-sibling::ol[1]')
                for w in winners.xpath('li'):
                    wdata = {}
                    wdata['link'] = BASE_URL + w.xpath('a/@href').extract()[0]
                    # process winners bio here
                    request = scrapy.Request(wdata['link'],
                                             callback=self.get_mini_bio)
                    request.meta['item'] = NWinnerItemBio(**wdata)
                    yield request

    def get_mini_bio(self, response):
        """ Get the winner's bio-text and photo. """

        item = response.meta['item']
        item['image_urls'] = []
        img_src = response.xpath(
            '//table[contains(@class, "biography")]//img/@src')
        if img_src:
            item['image_urls'] = ['https:' + img_src[0].extract()] # img src from wikipedias are relative, sorta
        mini_bio = ''
        paras = response.xpath(
            '//*[@id="mw-content-text"]/div[1]/p[string-length(normalize-space()) > 0 or not(normalize-space())]'
            #'//*[@id="mw-content-text"]/div[1]/p[text() or "normalize-space(.)=""]'
        ).extract() # could need tinkering

        for p in paras:
            mini_bio += p # may need work

        # correct for wiki-links

        mini_bio = mini_bio.replace('href="#', item['link'] + '#')
        item['mini_bio'] = mini_bio
        yield item


