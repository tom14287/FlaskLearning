
import unittest
from app.auth.views  import register_func
from app.auth.views import login_func
from test import MyTestRunner
import os
import tempfile
from app import db
from run import app
from flask_sqlalchemy import SQLAlchemy
import pymysql
from app.sql_operation.mysql import User


class TestStringMethods(unittest.TestCase):
   
    @classmethod
    def setUpClass(cls):
        app.config['SERVER_NAME'] = '127.0.0.1:5000'
        cls.client = app.test_client()

    def setUp(self):

        self.app_context = app.app_context()
        self.app_context.push()
        self.test_request_conext = app.test_request_context()


    def tearDown(self):
        self.app_context.pop()


    def test_Register_statement(self):
        with app.test_request_context():
            self.assertEqual(register_func(None,None,None,None,None), 'INPUTERR')
            self.assertEqual(register_func('test','test@163.com','12','123','0'), 'PWDERR')
            self.assertEqual(register_func('test1','already@163.com','123','123','1'),'SUCCEED')
            self.assertEqual(register_func('test2','already@163.com','12','12','1'),'REPEAT')


    def test_Register_condition_combination(self):
        with app.test_request_context():
            self.assertEqual(register_func(None,None,None,None,None), 'INPUTERR')
            self.assertEqual(register_func(None,None,None,None,'0'), 'INPUTERR')
            self.assertEqual(register_func(None,None,None,'123',None), 'INPUTERR')
            self.assertEqual(register_func(None,None,None,'123','0'), 'INPUTERR')
            self.assertEqual(register_func(None,None,'123',None,None), 'INPUTERR')
            self.assertEqual(register_func(None,None,'123',None,'0'), 'INPUTERR')
            self.assertEqual(register_func(None,None,'123','123',None), 'INPUTERR')
            self.assertEqual(register_func(None,None,'123','123','0'), 'INPUTERR')
            self.assertEqual(register_func(None,'test@163.com',None,None,None), 'INPUTERR')
            self.assertEqual(register_func(None,'test@163.com',None,None,'0'), 'INPUTERR')
            self.assertEqual(register_func(None,'test@163.com',None,'123',None), 'INPUTERR')
            self.assertEqual(register_func(None,'test@163.com',None,'123','0'), 'INPUTERR')
            self.assertEqual(register_func(None,'test@163.com','123',None,None), 'INPUTERR')
            self.assertEqual(register_func(None,'test@163.com','123',None,'0'), 'INPUTERR')
            self.assertEqual(register_func(None,'test@163.com','123','123',None), 'INPUTERR')
            self.assertEqual(register_func(None,'test@163.com','123','123','0'), 'INPUTERR')
            self.assertEqual(register_func('test',None,None,None,None), 'INPUTERR')
            self.assertEqual(register_func('test',None,None,None,'0'), 'INPUTERR')
            self.assertEqual(register_func('test',None,None,'123',None), 'INPUTERR')
            self.assertEqual(register_func('test',None,None,'123','0'), 'INPUTERR')
            self.assertEqual(register_func('test',None,'123',None,None), 'INPUTERR')
            self.assertEqual(register_func('test',None,'123',None,'0'), 'INPUTERR')
            self.assertEqual(register_func('test',None,'123','123',None), 'INPUTERR')
            self.assertEqual(register_func('test',None,'123','123','0'), 'INPUTERR')
            self.assertEqual(register_func('test','test@163.com',None,None,None), 'INPUTERR')
            self.assertEqual(register_func('test','test@163.com',None,None,'0'), 'INPUTERR')
            self.assertEqual(register_func('test','test@163.com',None,'123',None), 'INPUTERR')
            self.assertEqual(register_func('test','test@163.com',None,'123','0'), 'INPUTERR')
            self.assertEqual(register_func('test','test@163.com','123',None,None), 'INPUTERR')
            self.assertEqual(register_func('test','test@163.com','123',None,'0'), 'INPUTERR')
            self.assertEqual(register_func('test','test@163.com','123','123',None), 'INPUTERR')
            self.assertEqual(register_func('test','test@163.com','123','12','0'), 'PWDERR')
            self.assertEqual(register_func('testsuccess','test@163.com','123','123','0'), 'SUCCEED')
            self.assertEqual(register_func('testrepeat','test@163.com','123','123','0'), 'REPEAT')
    

    def test_login_statement(self):
        with app.test_request_context():
            self.assertEqual(login_func('not_exist@163.com',None),'NOACCOUNT')
            self.assertEqual(login_func('already@163.com','123'),'SUCCEED')
            self.assertEqual(login_func('already@163.com','321'),'WRONGPWD')


if __name__ == '__main__':
    unittest.main(testRunner=MyTestRunner())