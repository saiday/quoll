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

    def insert(self, query, args=None):
        try:
            self.cursor.execute(query, args)
            self.connect.commit()
            return self.cursor.lastrowid
        except:
            self.connect.rollback()

    def update(self, query, args=None):
        try:
            self.cursor.execute(query, args)
            self.connect.commit()
        except:
            self.connect.rollback()

    def is_exist(self, query, args=None):
        self.cursor.execute(query, args)
        return self.cursor.fetchone()


    def process_item(self, item, spider):
        query = """SELECT * FROM event WHERE url = %s"""
        exist = self.is_exist(query, item['url'])
        if not exist:
            venue_exist_query = """SELECT * FROM venue WHERE name = %s"""
            venue_exist = self.is_exist(venue_exist_query, item['venue'])
            if not venue_exist:
                venue_insert_query = """INSERT INTO venue(name, address) VALUES (%s, %s)"""
                venue_id = self.insert(venue_insert_query, (item['venue'], item['address']))
            else:
                venue_id = venue_exist.id

            event_insert_query = """
                            INSERT INTO event(title, url, image, body, date, time, venue_id, price) VALUES
                            (%s, %s, %s, %s, %s, %s, %s, %s)
                            """
            self.insert(event_insert_query, (
                        item['title'],
                        item['url'],
                        item['image'],
                        item['body'],
                        item['date'],
                        item['time'],
                        venue_id,
                        item['price']))
        else:
            # would not updating venue
            event_update_query = """
                        UPDATE event set title = %s, url = %s, image = %s, body = %s, date = %s, time = %s, price = %s
            """
            self.update(event_update_query, (
                        item['title'],
                        item['rul'],
                        item['image'],
                        item['body'],
                        item['date'],
                        item['time'],
                        item['price']))

        return item
