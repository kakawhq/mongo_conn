# -*- coding: utf-8 -*-


import pymongo
import conf


class Singleton(type):
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls._instance = None
    def __call__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__call__(*args, **kw)
        return cls._instance


#client单例        
class Client(object):
    __metaclass__ = Singleton
    def __init__(self):
        self.client = pymongo.MongoClient(conf.db_host, 27017)  #, maxPoolSize = 200)
        
    def init_col(self, db):
        self.db = self.client[db]
        def get_col(col):
            col = self.db[col]
            return col
        return get_col

       
    def find_data(self, f, **kw):
        self.Cur = f.find(
                filter = kw.get('filter'),
                projection = kw.get('projection', {'_id': 0}),
                skip = kw.get('skip', 0),
                limit = kw.get('limit', 0),
                no_cursor_timeout = kw.get('no_cursor_timeout', False),
                cursor_type = kw.get('cursor_type', pymongo.cursor.CursorType.NON_TAILABLE),
                sort = kw.get('sort'),
                allow_partial_results = kw.get('allow_partial_results', False),
                oplog_replay = kw.get('oplog_replay', False),
                modifiers = kw.get('modifiers'),
                manipulate = kw.get('manipulate', True)
        )
        return (i for i in self.Cur)

        

    def insert_one_data(self, f, **kw):
        self.Res = f.insert_one(
                kw.get('document'),
                kw.get('bypass_document_validation', False)
        )
        yield self.Res.acknowledged



    def insert_many_data(self, f, **kw):
        self.Res = f.insert_many(
                kw.get('documents'),
                kw.get('ordered', True),
                kw.get('bypass_document_validation', False)
        )
        yield self.Res.acknowledged
        


    def update_one_data(self, f, **kw):
        self.Res = f.update_one(
                kw.get('filter'),
                kw.get('update'),
                kw.get('upsert', False),
                kw.get('bypass_document_validation', False)
        )
        yield self.Res.raw_result
        

        
    def aggregate_data(self, f, **kw):
        self.Cur = f.aggregate(
                kw.get('pipeline')
        )
        return (i for i in self.Cur)
       
     
     
    def delete_one_data(self, f, **kw):
        self.Res = f.delete_one(
                kw.get('filter')
        )
        yield self.Res.raw_result
        
        
        
    def delete_many_data(self, f, **kw):
        self.Res = f.delete_many(
                kw.get('filter')
        )
        yield self.Res.raw_result
        
        
     
    def count_data(self, f, **kw):
        self.Res = f.count(
                filter = kw.get('filter'),
                limit = kw.get('limit'),
                skip = kw.get('skip'),
                maxTimeMS = kw.get('maxTimeMS')
        )
        yield self.Res