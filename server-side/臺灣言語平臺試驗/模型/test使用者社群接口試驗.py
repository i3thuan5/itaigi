# -*- coding: utf-8 -*-
from django.http.request import HttpRequest
from django.test import TestCase
from unittest.mock import Mock


from 臺灣言語平臺.使用者模型 import 使用者表
from 臺灣言語平臺.使用者模型 import 使用者社群接口


class 使用者社群接口試驗(TestCase):

    def setUp(self):
        self.社群接口 = 使用者社群接口()

    def tearDown(self):
        pass

    def 無表設定(self):
        登入資料 = Mock()
        登入資料.user = 使用者表(email='sui2@pigu.tw')
        self.使用者 = self.社群接口.save_user(HttpRequest(), 登入資料)

    def test_無表設定愛有email(self):
        self.無表設定()
        self.assertEqual(self.使用者.email, 'sui2@pigu.tw')

    def test_無表設定密碼愛鎖起來(self):
        self.無表設定()
        self.assertFalse(self.使用者.has_usable_password())

    def test_無表設定愛有名(self):
        self.無表設定()
        self.assertEqual(self.使用者.來源.名, 'sui2@pigu.tw')

    def test_無表來源有使用者資料紀錄(self):
        self.無表設定()
        self.assertEqual(self.使用者.來源.使用者, self.使用者)

    def 有表設定(self):
        登入資料 = Mock()
        登入資料.user = 使用者表()
        資料表 = Mock()
        資料表.cleaned_data = {
            'first_name': '古錐',
            'last_name': '蔡',
            'email': 'sui2@pigu.tw',
        }
        self.使用者 = self.社群接口.save_user(HttpRequest(), 登入資料, 資料表)

    def test_有表設定愛有email(self):
        self.有表設定()
        self.assertEqual(self.使用者.email, 'sui2@pigu.tw')

    def test_有表設定密碼愛鎖起來(self):
        self.有表設定()
        self.assertFalse(self.使用者.has_usable_password())

    def test_有表設定愛有名(self):
        self.有表設定()
        self.assertEqual(self.使用者.來源.名, '蔡古錐')

    def test_有表來源有使用者資料紀錄(self):
        self.有表設定()
        self.assertEqual(self.使用者.來源.使用者, self.使用者)

    def test_有表設定有name(self):
        登入資料 = Mock()
        登入資料.user = 使用者表()
        資料表 = Mock()
        資料表.cleaned_data = {
            'name': '蔡古錐',
            'email': 'sui2@pigu.tw',
        }
        self.使用者 = self.社群接口.save_user(HttpRequest(), 登入資料, 資料表)
        self.assertEqual(self.使用者.來源.名, '蔡古錐')

    def test_有表設定有username(self):
        登入資料 = Mock()
        登入資料.user = 使用者表()
        資料表 = Mock()
        資料表.cleaned_data = {
            'username': '蔡古錐',
            'email': 'sui2@pigu.tw',
        }
        self.使用者 = self.社群接口.save_user(HttpRequest(), 登入資料, 資料表)
        self.assertEqual(self.使用者.來源.名, '蔡古錐')

    def test_有表設定無name用email(self):
        登入資料 = Mock()
        登入資料.user = 使用者表()
        資料表 = Mock()
        資料表.cleaned_data = {
            'email': 'sui2@pigu.tw',
        }
        self.使用者 = self.社群接口.save_user(HttpRequest(), 登入資料, 資料表)
        self.assertEqual(self.使用者.來源.名, 'sui2@pigu.tw')

    def test_有表設定空name用email(self):
        登入資料 = Mock()
        登入資料.user = 使用者表()
        資料表 = Mock()
        資料表.cleaned_data = {
            'name': '',
            'email': 'sui2@pigu.tw',
        }
        self.使用者 = self.社群接口.save_user(HttpRequest(), 登入資料, 資料表)
        self.assertEqual(self.使用者.來源.名, 'sui2@pigu.tw')

    def test_補使用者資料檢查email(self):
        登入資料 = Mock()
        登入資料.user = 使用者表()
        self.使用者 = self.社群接口.populate_user(HttpRequest(), 登入資料, {
            'name': '蔡古錐',
            'email': 'sui2@pigu.tw',
        })
        self.assertEqual(self.使用者.email, 'sui2@pigu.tw')

    def test_補使用者資料有name(self):
        登入資料 = Mock()
        登入資料.user = 使用者表()
        self.使用者 = self.社群接口.populate_user(HttpRequest(), 登入資料, {
            'name': '蔡古錐',
            'email': 'sui2@pigu.tw',
        })
        self.assertEqual(self.使用者.來源.名, '蔡古錐')

    def test_補使用者資料有username(self):
        登入資料 = Mock()
        登入資料.user = 使用者表()
        self.使用者 = self.社群接口.populate_user(HttpRequest(), 登入資料, {
            'username': '蔡古錐',
            'email': 'sui2@pigu.tw',
        })
        self.assertEqual(self.使用者.來源.名, '蔡古錐')

    def test_補使用者資料有姓名(self):
        登入資料 = Mock()
        登入資料.user = 使用者表()
        self.使用者 = self.社群接口.populate_user(HttpRequest(), 登入資料, {
            'first_name': '古錐',
            'last_name': '蔡',
            'email': 'sui2@pigu.tw',
        })
        self.assertEqual(self.使用者.來源.名, '蔡古錐')

    def test_補使用者資料無name(self):
        登入資料 = Mock()
        登入資料.user = 使用者表()
        self.使用者 = self.社群接口.populate_user(HttpRequest(), 登入資料, {
            'email': 'sui2@pigu.tw',
        })
        self.assertEqual(self.使用者.來源.名, 'sui2@pigu.tw')

    def test_補使用者資料空name(self):
        登入資料 = Mock()
        登入資料.user = 使用者表()
        self.使用者 = self.社群接口.populate_user(HttpRequest(), 登入資料, {
            'first_name': '',
            'last_name': '',
            'email': 'sui2@pigu.tw',
        })
        self.assertEqual(self.使用者.來源.名, 'sui2@pigu.tw')

    def test_註冊愛開起來(self):
        self.assertTrue(
            self.社群接口.is_open_for_signup(HttpRequest(), None)
        )
