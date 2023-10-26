import scrapy
import re

BASE_URL = "https://en.wikipedia.org"


# x path to get to a winners wikidata bio page
# //*[@id="t-wikibase"]/a

class NWinnerItem(scrapy.Item):
    """ Defines Nobel winner data to be Scraped. """
    name = scrapy.Field()
    link = scrapy.Field()
    year = scrapy.Field()
    category = scrapy.Field()
    country = scrapy.Field()
    gender = scrapy.Field()
    born_in = scrapy.Field()
    date_of_birth = scrapy.Field()
    date_of_death = scrapy.Field()
    place_of_birth = scrapy.Field()
    place_of_death = scrapy.Field()
    text = scrapy.Field()


class NWinnerSpider(scrapy.Spider):
    """ Scrapes the country and link text of the Nobel-winners. """

    name = 'nwinners_list'
    allowed_domains = ['en.wikipedia.org', 'www.wikidata.org']
    start_urls = [
        "https://en.wikipedia.org/wiki/List_of_Nobel_laureates_by_country"
    ]

    def parse(self, response):

        h3s = response.xpath('//h3')

        for h3 in h3s:
            country = h3.xpath('span[@class="mw-headline"]/text()').extract()
            if country:
                winners = h3.xpath('following-sibling::ol[1]')
                for w in winners.xpath('li'):
                    wdata = self.process_winner_li(w, country[0])
                    request = scrapy.Request(
                        wdata['link'],
                        callback=self.parse_bio,
                        dont_filter=True)
                    request.meta['item'] = NWinnerItem(**wdata)
                    yield request

    def process_winner_li(self, w, country=None):
        """
        Process a winner's <li> tag, adding country of birth
        or nationality, as applicable.
        """
        wdata = {}
        wdata['link'] = BASE_URL + w.xpath('a/@href').extract()[0]
        text = ' '.join(w.xpath('descendant-or-self::text()').extract())

        # get comma delineated name and strip trailing whitespace
        wdata['name'] = text.split(',')[0].strip()

        year = re.findall('\d{4}', text)
        if year:
            wdata['year'] = int(year[0])
        else:
            wdata['year'] = 0
            print('Oops, no year in ', text)

        category = re.findall(
            'Physics|Chemistry|Physiology or Medecine|Literature|Peace|Economics', text
        )

        if category:
            wdata['category'] = category[0]
        else:
            wdata['category'] = ''
            print('Oops, no category in ', text)

        if country:
            if text.find('*') != -1:
                wdata['country'] = ''
                wdata['born_in'] = country
            else:
                wdata['country'] = country
                wdata['born_in'] = ''
        # store a copy of link's text for any manual corrections
        wdata['text'] = text
        return wdata

    def parse_bio(self, response):
        item = response.meta['item']
        href = response.xpath("//*[@id='t-wikibase']/a/@href").extract()
        # //*[@id="t-wikibase"]/a
        if href:
            request = scrapy.Request(
                href[0],
                callback=self.parse_wikidata,
                dont_filter=True)
            request.meta['item'] = item
            yield request

    def parse_wikidata(self, response):
        item = response.meta['item']
        property_codes = [
            {'name': 'date_of_birth', 'code': 'P569'},
            {'name': 'date_of_death', 'code': 'P570'},
            {'name': 'place_of_birth', 'code': 'P19', 'link': True},
            {'name': 'place_of_death', 'code': 'P20', 'link': True},
            {'name': 'gender', 'code': 'P21', 'link': True},
        ]

        # xpath_row = '//*[@id="{code}"]'
        # xpath_value = '/div[2]/div/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/text()'
        p_template = '//*[@id="{code}"]/div[2]/div/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/text()'
        # ex: '//*[@id="P569"]/div[2]/div/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/text()'
        for prop in property_codes:
            link_html = ''
            if prop.get('link'):
                link_html = '/a'
            sel = response.xpath(
                p_template.format(code=prop['code'],link_html=link_html))
            if sel:
                item[prop['name']] = sel[0].extract()

            yield item
