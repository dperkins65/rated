import os
import unittest
from app import create_app
from app.database import db


class TestCase(unittest.TestCase):
    def setUp(self):
        app = create_app('UnitTestConfig')
        db.app = app
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_404(self):
        resp = self.app.get('/fail', follow_redirects=True)
        assert resp.status_code == 404
        assert b'File Not Found' in resp.data

    def test_login(self):
        resp = self.app.get('/login', follow_redirects=True)
        assert resp.status_code == 200
        assert b'Please sign in' in resp.data
