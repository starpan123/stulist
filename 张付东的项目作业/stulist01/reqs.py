# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web

from dbconn import db_cursor

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("pages/main.html")


class StudentListHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("pages/stu_list.html", students = dal_list_students())

class StudentEditHandler(tornado.web.RequestHandler):
    def get(self, stu_sn):

        stu = None
        if stu_sn != 'new' :
            stu = dal_get_student(stu_sn)
        
        if stu is None:
            stu = dict(stu_sn='new', sno='', sname='', sex='',sbir='',cla='')

        self.render("pages/stu_edit.html", student = stu)

    def post(self, stu_sn):
        sno = self.get_argument('sno','')
        sname = self.get_argument('sname', '')
        sex = self.get_argument('sex', '')
        sbir = self.get_argument('sbir','')
        cla = self.get_argument('cla','')

        if stu_sn == 'new' :
            dal_create_student(sno, sname, sex,sbir,cla)
        else:
            dal_update_student(stu_sn, sno, sname, sex, sbir, cla)

        self.redirect('/stulist')

class StudentDelHandler(tornado.web.RequestHandler):
    def get(self, stu_sn):
        dal_del_student(stu_sn)
        self.redirect('/stulist')

# -------------------------------------------------------------------------

def dal_list_students():
    data = []
    with db_cursor() as cur : # 取得操作数据的游标，记为cur
        s = """
        SELECT stu_sn, sno, sname, sex,sbir,cla FROM student ORDER BY stu_sn DESC
        """
        cur.execute(s)      
        for r in cur.fetchall():
            stu = dict(stu_sn=r[0], sno=r[1], sname=r[2], sex=r[3],sbir=r[4],cla=r[5])
            data.append(stu)
    return data


def dal_get_student(stu_sn):
    with db_cursor() as cur : # 取得操作数据的游标，记为cur
        s = """
        SELECT stu_sn, sno, sname, sex,sbir,cla FROM student WHERE stu_sn=%s
        """
        cur.execute(s, (stu_sn, ))
        r = cur.fetchone()
        if r :
            return dict(stu_sn=r[0], sno=r[1], sname=r[2], sex=r[3],sbir=r[4],cla=r[5])


def dal_create_student(sno, sname, sex,sbir,cla):
    with db_cursor() as cur : # 取得操作数据的游标，记为cur
        cur.execute("SELECT nextval('seq_stu_sn')")
        stu_sn = cur.fetchone()
        assert stu_sn is not None

        print('新学生内部序号%d: ' % stu_sn)

        s = """
        INSERT INTO student (stu_sn, sno, sname, sex,sbir,cla) 
        VALUES (%(stu_sn)s, %(sno)s, %(sname)s, %(sex)s, %(sbir)s, %(cla)s)
        """
        cur.execute(s, dict(stu_sn=stu_sn, sno=sno, sname=sname, sex=sex, sbir=sbir, cla=cla))


def dal_update_student(stu_sn, sno, sname, sex,sbir,cla):
    with db_cursor() as cur : # 取得操作数据的游标，记为cur
        s = """
        UPDATE student SET
          sno=%(sno)s, 
          sname=%(sname)s, 
          sex=%(sex)s, 
          sbir=%(sbir)s, 
          cla=%(cla)s
        WHERE stu_sn=%(stu_sn)s
        """
        cur.execute(s, dict(stu_sn=stu_sn, sno=sno, sname=sname, sex=sex, sbir=sbir, cla=cla))


def dal_del_student(stu_sn):
    with db_cursor() as cur : # 取得操作数据的游标，记为cur
        s = """
        DELETE FROM student WHERE stu_sn=%(stu_sn)s
        """
        cur.execute(s, dict(stu_sn=stu_sn))
        print('删除%d条记录' % cur.rowcount)
