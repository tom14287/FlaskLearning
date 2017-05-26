import os
import unittest
import tempfile
import app

class FlaskTestCase(unittest.TestCase):
	def setUp(self):
		self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
		app.app.config['TESTING'] = True
		self.app = app.app.test_client()


	def tearDown(self):
		os.close(self.db_fd)
		os.unlink(app.app.config['DATABASE'])



if __name__ == '__main__':
	unittest.main()
