# -*- coding: utf-8 -*-
from django.test import TestCase
from 臺灣言語平臺.使用者模型 import 使用者表管理
from datetime import datetime
from unittest.mock import patch
from django.utils import timezone


class 使用者表管理試驗(TestCase):

    def setUp(self):
        self.這馬時間patcher = patch('django.utils.timezone.now')
        這馬時間mock = self.這馬時間patcher.start()
        這馬時間mock.return_value = datetime(2012, 12, 28, tzinfo=timezone.utc)
        管理 = 使用者表管理()
        self.使用者 = 管理.create_superuser('sui2@pigu.tw', 'I\'m sui2')

    def tearDown(self):
        self.這馬時間patcher.stop()

    def test_檢查email(self):
        self.assertEqual(self.使用者.email, 'sui2@pigu.tw')

    def test_檢查名(self):
        self.assertEqual(self.使用者.來源.名, 'sui2@pigu.tw')

    def test_檢查密碼愛hash(self):
        self.assertNotEqual(self.使用者.password, '')
        self.assertNotEqual(self.使用者.password, 'I\'m sui2')

    def test_檢查管理員(self):
        self.assertTrue(self.使用者.is_staff)

    def test_有註冊時間(self):
        self.使用者.註冊時間

    def test_註冊時間(self):
        self.assertEqual(
            self.使用者.註冊時間, datetime(2012, 12, 28, tzinfo=timezone.utc))
