# -*- coding: utf-8 -*-

import gevent.monkey as monkey; monkey.patch_all()  
#import gevent.wsgi  
import gevent
import web
import mongo_func
import conf
import json
import collections


#####################################
urls = (
    "/", "index",
    "/mymongo/(.+)", "Control",    #<host>:<port>/mymongo/<func>/<db>/<collection>
)



######################################
class index:
    def GET(self):
        res = "gg"
        #gevent.sleep(0)
        return res
        

# 调用mongo_func中定义的方法        
class Control(mongo_func.Client):
    def __init__(self):   
        super(Control, self).__init__()
        
    def GET(self, n):
        return n
    
    def POST(self, n):
        try:
            post_data = json.loads(web.data())
            n = n.split('/')    #[func, db, collection]
            if post_data and len(n) == 3 and hasattr(self, n[0]):
                dofunc = getattr(self, n[0])
                res = dofunc(self.init_col(n[1])(n[2]), **post_data)
            else:
                res = ['request error']   #请求参数错误
            gevent.sleep(0)
            return json.dumps({'resdata': tuple(res) if res else 0})
        except Exception as e:
            print e
            return 'error'
   
'''
# 直接调用pymongo的collection中的方法   
class Col(mongo_func.Client):
    def __init__(self):
        super(Control, self).__init__()
    
    def GET(self, n):
        return n
    
    def POST(self, n):
        post_data = json.loads(web.data())
        try:
            n = n.split('/')
            if len(n) == 3 and post_data:
                _func, _db, _collection = n[0], n[1], n[2]
                col_obj = self.init_col(_db)(_collection)
                if hasattr(col_obj, _func):
                    dofunc = getattr(col_obj, _func)               
                    _func == 'find' and post_data.setdefault('projection', {'_id': 0})   
                    cur = dofunc(**post_data)
                else:
                    cur = 'function {0} is not defined'.format(_func)
            else:
                cur = 'request error'
            gevent.sleep(0)
            return json.dumps({'resdata': tuple(i for i in cur) if isinstance(cur, collections.Iterator) else cur, 'cli': id(self.client)})
        except Exception as e:
            print e
            return 0
'''

   
#if __name__ == "__main__":  
app = web.application(urls, globals())
application = app.wsgifunc()  
#    print 'Serving on 8088...'  
#    gevent.wsgi.WSGIServer(('', 8088), application).serve_forever()
        
