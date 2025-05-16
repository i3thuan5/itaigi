# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase


from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語平臺.使用者模型 import 使用者表


class 使用者表試驗(TestCase):

    def test_有email佮來源(self):
        來源內容 = {"名": '鄉民', '出世年': '1950', '出世地': '臺灣', }
        來源 = 來源表.加來源(來源內容)
        使用者 = 使用者表(email='sui2@pigu.tw', 來源=來源)
        使用者.set_unusable_password()
        使用者.full_clean()

    def test_愛有email(self):
        來源內容 = {"名": '鄉民', '出世年': '1950', '出世地': '臺灣', }
        來源 = 來源表.加來源(來源內容)
        使用者 = 使用者表(來源=來源)
        使用者.set_unusable_password()
        self.assertRaises(ValidationError, 使用者.full_clean,)

    def test_愛有來源(self):
        使用者 = 使用者表(email='sui2@pigu.tw')
        使用者.set_unusable_password()
        self.assertRaises(ValidationError, 使用者.full_clean,)

# 	加使用者
    def 加鄉民使用者(self):
        來源內容 = {"名": '鄉民', '出世年': '1950', '出世地': '臺灣', }
        return 使用者表.加使用者('sui2@pigu.tw', 來源內容,)

    def test_加使用者(self):
        使用者 = self.加鄉民使用者()
        self.assertEqual(使用者.來源.編號(), 使用者.編號())

    def test_重覆email(self):
        self.加鄉民使用者()
        來源內容 = {"名": '鄉民', '出世年': '1950', '出世地': '臺灣', }
        self.assertRaises(IntegrityError, 使用者表.加使用者, 'sui2@pigu.tw', 來源內容,)

    def test_密碼愛鎖起來(self):
        使用者 = self.加鄉民使用者()
        self.assertFalse(使用者.has_usable_password())

    def test_來源有使用者資料記錄(self):
        使用者 = self.加鄉民使用者()
        self.assertEqual(
            使用者.來源.使用者,
            使用者
        )
