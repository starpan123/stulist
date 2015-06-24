#! /usr/bin/env python3
# -*- coding:UTF-8 -*-

from dbconn import db_cursor

def create_db():
    sqlstr = """
    DROP TABLE IF EXISTS student;

    CREATE TABLE IF NOT EXISTS student  (
        stu_sn   INTEGER,     --序号
        sno      TEXT,        --学号
        sname    TEXT,        --姓名
        sex      TEXT,        --性别
        sbir     TEXT,        --出生日期
        cla      TEXT,        --班级
        PRIMARY KEY(stu_sn)
    );
    -- CREATE UNIQUE INDEX idx_student_no ON student(sno);

    CREATE SEQUENCE seq_stu_sn 
        START 10000 INCREMENT 1 OWNED BY student.stu_sn;

    """
    with db_cursor() as cur :
        cur.execute(sqlstr) # 执行SQL语句
    
def init_data():
    sqlstr = """
    DELETE FROM student;

    INSERT INTO student (stu_sn, sno, sname,sex,sbir,cla)  VALUES 
        (101, '1310650101',  '齐琪','男','1994-1-1','信息1301'), 
        (102, '1310650304',  '张付东','男','1994-2-1','信息1303'),
        (103, '1310650106',  '潘星','男','1994-3-1','信息1301'),
        (104, '1310650116',  '蔺珍妮','女','1994-4-1','信息1301'),
        (105, '1310650117',  '王潇懿','女','1994-5-1','信息1301'),
        (106, '1310650119',  '张欣怡','女','1994-6-1','信息1301');



    """
    with db_cursor() as cur :
        cur.execute(sqlstr)    

if __name__ == '__main__':
    create_db()
    init_data()
    print('数据库已初始化完毕！')

