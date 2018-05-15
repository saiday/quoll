# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging

import pymysql

from quoll import settings


class QuollPipeline(object):

    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            password=settings.MYSQL_PASSWORD,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:
            query = """select * from event where url = %s"""
            self.cursor.execute(query, item['url'])
            exist = self.cursor.fetchone()
            if exist:
                self.cursor.execute("""update event set title = %s, url = %s, image = %s, body = %s, date = %s, time = %s, price = %s""",
                                    (item['title'],
                                     item['url'],
                                     item['image'],
                                     item['body'],
                                     item['date'],
                                     item['time'],
                                     item['price']))
            else:
                self.cursor.execute("""insert into event(title, url, image, body, date, time, price) value (%s, %s, %s, %s, %s, %s, %s)""",
                                    (item['title'],
                                     item['url'],
                                     item['image'],
                                     item['body'],
                                     item['date'],
                                     item['time'],
                                     item['price']))
            self.connect.commit()
        except Exception as error:
            # TODO: slack hook
            print(error)
            logging.critical(error)

        return item

    # def if_record_exist

