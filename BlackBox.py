
import unittest
from run import app
from app.auth import login_func, register_func
from test import MyTestRunner


class BlackBoxTest(unittest.TestCase):
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


	def test_login(self):
		with app.test_request_context():
			self.assertEqual(login_func("blackbox_consumer@qq.com", "test"), "SUCCEED","BlackBox-login success failed")
			self.assertEqual(login_func("notexist@qq.com", "default"), "NOACCOUNT", "BlackBox-login noaccount failed")
			self.assertEqual(login_func(None, "default"), "NOACCOUNT", "Black-login noaccount-failed")
			self.assertEqual(login_func("blackbox_consumer@qq.com", "default"), "WRONGPWD", "BlackBox-login wrongpwd failed")


	def test_Register(self):
		with app.test_request_context():

			self.assertEqual(register_func(None, "blackbox_consumer@qq.com", "test", "test", "Consumer"), "INPUTERR", "BlackBox-register inputerr failed")
			self.assertEqual(register_func("blackbox", None, "test", "test","Consumer"), "INPUTERR", "BlackBox-register inputerr failed")
			self.assertEqual(register_func("blackbox", "blackbox_consumer@qq.com", None, "test", "Consumer"), "INPUTERR","BlackBox-register inputerr failed")
			self.assertEqual(register_func("blackbox", "blackbox_consumer@qq.com", "test", None, "Consumer"), "INPUTERR","BlackBox-register inputerr failed")
			self.assertEqual(register_func("blackbox", "blackbox_consumer@qq.com", "test", "test", None), "INPUTERR","BlackBox-register inputerr failed")

			self.assertEqual(register_func("blackbox_designer", "blackbox_designer@qq.com", "test", "test", "Designer"), "SUCCEED", "BlackBox-register(designer) success failed")
			self.assertEqual(register_func("blackbox_company", "blackbox_company@qq.com", "test", "test", "Company"), "SUCCEED", "BlackBox-register(company) success failed")
			self.assertEqual(register_func("blackbox_consumer", "blackbox_consumer@qq.com", "test", "test", "Consumer"), "SUCCEED", "BlackBox-register(consumer) success failed")

			self.assertEqual(register_func("blackbox_consumer", "blackbox_consumer@qq.com", "test", "test", "Consumer"), "REPEAT", "BlackBox-register repeat failed")
			self.assertEqual(register_func("blackbox_new", "blackbox_new@qq.com", "test", "test1","Consumer"), "PWDERR", "BlackBox-register pwderr failed")

if __name__ == '__main__':
	unittest.main(testRunner=MyTestRunner())

