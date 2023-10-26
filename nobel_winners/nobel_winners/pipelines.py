# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# class NobelWinnersPipeline:
#     def process_item(self, item, spider):
#         return item

# useful for handling different item types with a single interface
#from itemadapter import ItemAdapter
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

class DropNonPersons(object):
    """ Remove non-person winners """

    def process_item(self, item, spider):
        if 'gender' not in item or not item['gender']:
            raise DropItem(f"No gender")
        return item

class NobelImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):

        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):

        image_paths = [x['path'] for ok, x in results if ok]
        if image_paths:
            item['bio_image'] = image_paths[0]
        return item

