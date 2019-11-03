# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class DangdangPipeline(object):

    def open_spider(self,spider):
        print('opened')
        try:
            self.con = pymysql.connect(host='localhost', port=3306, user='root', password='12345678', charset='utf8')
            self.cursor = self.con.cursor(pymysql.cursors.DictCursor)
            try:
                self.cursor.execute('create database dangdang')
            except:
                pass
            self.con.select_db('dangdang')
            try:
                self.cursor.execute('drop table books')
            except:
                pass
            try:
                sql='''
                    create table books(
                    bID varchar(8) primary key ,
                    bTitle varchar(512),
                    bAuthor varchar (256),
                    bPublisher varchar (256),
                    bDate varchar (32),
                    bPrice varchar (16),
                    bDetail text)
                '''
                self.cursor.execute(sql)
            except:
                self.cursor.execute('delete from books')
            self.opened = True
            self.count = 0
        except Exception as err:
            print(err)
            self.opened = False


    def close_spider(self,spider):
        if self.opened:
            self.con.commit()
            self.con.close()
            self.opened = False
        print('closed')
        print('总共爬取', self.count,'本书籍')


    def process_item(self, item, spider):
        try:
            print(item['title'])
            print(item['author'])
            print(item['publisher'])
            print(item['date'])
            print(item['price'])
            print(item['detail'])
            print()
            if self.opened:
                self.cursor.execute('insert into books(bID,bTitle,bAuthor,bPublisher,bDate,bPrice,bDetail)values(%s,%s,%s,%s,%s,%s,%s)',(item['id'],item['title'],item['author'],
                                                                                                                                  item['publisher'],item['date'],item['price'],item['detail']))
                self.count += 1
        except Exception as err:
            print(err)
        return item
