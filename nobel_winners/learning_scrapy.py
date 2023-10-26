
# commands run to setup project (cl, no ipython):
#   $ scrapy startproject 'nobel_winners'
#   $ cd nobel_winners
#   $ scrapy genspider example example.com
#
#   Enter a crapy shell that allows you to play with tools on a cached page
#   $ scrapy shell https://en.wikipedia.org/wiki/List_of_Nobel_laureates_by_country
#
# manually check the xpath to country headers in chrome dev tools
#   x path to country section headers for nobel laureate list
#   //*[@id="mw-content-text"]/div[1]/h3[1]    < first header
#   //*[@id="mw-content-text"]/div[1]/h3[2]    < second header
#
# in scrapy shell, get list of h3 elements, then extract data using xpath
#   h3s = response.xpath('//h3')
#   h3_arg = h3s[1]
#   country = h3_arg.xpath('span[@class="mw-headline"]/text()').extract()
#   --> ['Argentina']

# get the subsequent ol of winners from that country
#   ol_arg = h3_arg.xpath('following-sibling::ol[1]')
#   ol_arg = ol_arg[0]
# get the list items
#   lis_arg = ol_arg.xpath('li')
#   name = li.xpath('a//text()')[0].extract()
#   --> 'César Milstein'

# list_text = li.xpath('descendant-or-self::text()').extract()