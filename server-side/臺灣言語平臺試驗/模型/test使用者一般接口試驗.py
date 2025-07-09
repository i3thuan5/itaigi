# -*- coding: utf-8 -*-
from django.http.request import HttpRequest
from django.test import TestCase
from unittest.mock import Mock


from 臺灣言語平臺.使用者模型 import 使用者表
from 臺灣言語平臺.使用者模型 import 使用者一般接口


class 使用者一般接口試驗(TestCase):

    def setUp(self):
        self.一般接口 = 使用者一般接口()

    def tearDown(self):
        pass

    def 一般設定(self):
        資料表 = Mock()
        資料表.cleaned_data = {
            'first_name': '古錐',
            'last_name': '蔡',
            'email': 'sui2@pigu.tw',
        }
        self.使用者 = self.一般接口.save_user(HttpRequest(), 使用者表(), 資料表)

    def test_愛有email(self):
        self.一般設定()
        self.assertEqual(self.使用者.email, 'sui2@pigu.tw')

    def test_密碼愛鎖起來(self):
        self.一般設定()
        self.assertFalse(self.使用者.has_usable_password())

    def test_愛有名(self):
        self.一般設定()
        self.assertEqual(self.使用者.來源.名, '蔡古錐')

    def test_來源有使用者資料紀錄(self):
        self.一般設定()
        self.assertEqual(self.使用者.來源.使用者, self.使用者)

    def test_有username(self):
        資料表 = Mock()
        資料表.cleaned_data = {
            'first_name': '古錐',
            'last_name': '蔡',
            'username': '姑娘',
            'email': 'sui2@pigu.tw',
        }
        self.使用者 = self.一般接口.save_user(HttpRequest(), 使用者表(), 資料表)
        self.assertEqual(self.使用者.來源.名, '姑娘')

    def test_無name用email(self):
        資料表 = Mock()
        資料表.cleaned_data = {
            'email': 'sui2@pigu.tw',
        }
        self.使用者 = self.一般接口.save_user(HttpRequest(), 使用者表(), 資料表)
        self.assertEqual(self.使用者.來源.名, 'sui2@pigu.tw')

    def test_空name用email(self):
        資料表 = Mock()
        資料表.cleaned_data = {
            'first_name': '',
            'last_name': '',
            'username': '',
            'email': 'sui2@pigu.tw',
        }
        self.使用者 = self.一般接口.save_user(HttpRequest(), 使用者表(), 資料表)
        self.assertEqual(self.使用者.來源.名, 'sui2@pigu.tw')

    def test_有密碼(self):
        資料表 = Mock()
        資料表.cleaned_data = {
            'email': 'sui2@pigu.tw',
            'password1': 'I\'m sui2',
        }
        self.使用者 = self.一般接口.save_user(HttpRequest(), 使用者表(), 資料表)
        self.assertTrue(self.使用者.has_usable_password())

    def test_註冊關起來(self):
        self.assertFalse(
            self.一般接口.is_open_for_signup(HttpRequest())
        )
