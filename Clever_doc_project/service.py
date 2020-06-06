#!/usr/bin/env python

from calc_queue import Calculation

import tornado.web
import tornado.ioloop


SERVICE_PORT = 8888

class Index(tornado.web.RequestHandler):
    def get(self):
        self.write(str(self.application.calcul_request.call(self, "3+10")))
        self.render('index.html')


app = tornado.web.Application([
        (r'/', Index),
    ])

def main():
    loop = tornado.ioloop.IOLoop.current()
    calcul_request = Calculation()
    app.calcul_request = calcul_request
    app.calcul_request.connect()
    app.listen(SERVICE_PORT)
    print(" port of service : %d" % SERVICE_PORT)
    loop.start()


if __name__ == '__main__':
    main()
