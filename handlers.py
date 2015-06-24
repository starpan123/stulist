# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web

from dbconn import db_stulist

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("pages/main.html")


class StudentListHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("pages/stu_list.html", students = dal_list_students())


def dal_list_students():
    data = []
    with db_cursor() as cur : # 取得操作数据的游标，记为cur
        s = """
        SELECT stu_sn, sno, sname, sex, sbir, cla FROM student ORDER BY stu_sn
        """
        cur.execute(s)      
        for r in cur.fetchall():
            stu = dict(stu_sn=r[0], sno=r[1], sname=r[2], sex=r[3], sbir=r[4], cla=r[5])
            data.append(stu)
    print(data)
    return data

