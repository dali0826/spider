# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from pymongo import MongoClient
from mongoengine import *
from maoyan.models import Movie


#mysql
class MaoyanPipeline(object):

    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get("MYSQL_HOST"),
            database=crawler.settings.get("MYSQL_DATABASE"),
            user=crawler.settings.get("MYSQL_USER"),
            password=crawler.settings.get("MYSQL_PASSWORD"),
            port=crawler.settings.get("MYSQL_PORT"),
        )

    def open_spider(self, spider):
        self.db = pymysql.connect(self.host, self.user, self.password, self.database, charset='utf8', port=self.port)
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        sql='insert into movies (name,star,release_time,score) ' \
            'values ("%s","%s","%s","%s")' \
            %(item['name'],item['star'],item['release_time'],item['score'])
        self.cursor.execute(sql)
        self.db.commit()
        return item



#mongodb
class MaoyanMonGoDBPipeline(object):

    def __init__(self,database):
        self.db=database

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            database=crawler.settings.get('MONGO_DB'),
        )

    def open_spider(self, spider):
        connect(self.db)

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        movie=Movie()
        movie.name=item['name']
        movie.star=item['star']
        movie.release_time=item['release_time']
        movie.score=item['score']
        movie.save()

        return item



#PyMonGo
class MaoyanPyMonGoDBPipeline(object):

    def __init__(self,database):
        self.client=MongoClient()
        self.db=self.client[database]

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            database=crawler.settings.get('MONGO_DB'),
        )

    def open_spider(self, spider):

        pass

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        movie={}
        movie['name']=item['name']
        movie['star']=item['star']
        movie['release_time']=item['release_time']
        movie['score']=item['score']
        self.db.movies.insert(movie)

        return item

