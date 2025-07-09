# -*- coding: utf-8 -*-
from django.test import TestCase
from 試驗.加關係.加關係試驗 import 加關係試驗
import json
from 臺灣言語資料庫.資料模型 import 聽拍表
from 臺灣言語資料庫.關係模型 import 聽拍校對表


class 加聽拍校對試驗(加關係試驗, TestCase):

    def setUp(self):
        self.加初始資料()
        self.原本資料表 = 聽拍表
        self.原本資料詞內容 = {
            '收錄者': json.dumps({'名': '鄉民', '出世年': '1950', '出世地': '臺灣'}),
            '來源': json.dumps({'名': 'Dr. Pigu', '出世年': '1990', '出世地': '花蓮人'}),
            '版權': '會使公開',
            '種類': '字詞',
            '語言腔口': '閩南語',
            '著作所在地': '花蓮',
            '著作年': '2014',
            '聽拍資料': [
                {'語者': '阿宏', '內容': 'li2', '開始時間': 0.0, '結束時間': 1.2},
                {'語者': '阿莉', '內容': 'ho2', '開始時間': 1.2, '結束時間': 2.0},
            ]
        }
        self.原本資料句內容 = {
            '收錄者': json.dumps({'名': '鄉民', '出世年': '1950', '出世地': '臺灣'}),
            '來源': json.dumps({'名': 'Dr. Pigu', '出世年': '1990', '出世地': '花蓮人'}),
            '版權': '會使公開',
            '種類': '語句',
            '語言腔口': '四縣話',
            '著作所在地': '花蓮',
            '著作年': '2014',
            '聽拍資料': [
                {'內容': '請問車頭按怎行？'},
                {'內容': '直直行就到了。'},
            ],
        }
        self.對應資料詞內容 = {
            '收錄者': json.dumps({'名': '鄉民', '出世年': '1950', '出世地': '臺灣'}),
            '來源': json.dumps({'名': 'Dr. Pigu', '出世年': '1990', '出世地': '花蓮人'}),
            '版權': '會使公開',
            '種類': '字詞',
            '語言腔口': '閩南語',
            '著作所在地': '花蓮',
            '著作年': '2014',
            '聽拍資料': [
                {'語者': '阿宏', '內容': 'li1', '開始時間': 0.0, '結束時間': 1.2},
                {'語者': '阿莉', '內容': 'ho2', '開始時間': 1.2, '結束時間': 2.0},
            ]
        }
        self.對應資料句內容 = {
            '收錄者': json.dumps({'名': 'Dr. Pigu', '出世年': '1990', '出世地': '花蓮人'}),
            '來源': json.dumps({'名': '鄉民', '出世年': '1950', '出世地': '臺灣'}),
            '版權': '袂使公開',
            '種類': '語句',
            '語言腔口': '四縣話',
            '著作所在地': '臺灣',
            '著作年': '195x',
            '聽拍資料': [
                {'內容': '請問車頭按怎行？'},
                {'內容': '直直行就到矣。'},
            ],
        }

    def 加詞(self, 原本聽拍):
        原來聽拍資料數 = 聽拍表.objects.all().count()
        原來聽拍校對數 = 聽拍校對表.objects.all().count()
        聽拍 = 原本聽拍.校對做(self.對應資料詞內容)
        self.assertEqual(聽拍表.objects.all().count(), 原來聽拍資料數 + 1)
        self.assertEqual(聽拍校對表.objects.all().count(), 原來聽拍校對數 + 1)
        self.assertIsInstance(原本聽拍.聽拍校對.get(新聽拍=聽拍), 聽拍校對表)
        self.assertEqual(原本聽拍.聽拍校對.get(新聽拍=聽拍).新聽拍, 聽拍)
        self.assertEqual(聽拍.收錄者.名, '鄉民')
        self.assertEqual(聽拍.收錄者.屬性內容(), {'出世年': '1950', '出世地': '臺灣'})
        self.assertEqual(聽拍.來源.名, 'Dr. Pigu')
        self.assertEqual(聽拍.來源.屬性內容(), {'出世年': '1990', '出世地': '花蓮人'})
        self.assertEqual(聽拍.版權.版權, '會使公開')
        self.assertEqual(聽拍.種類.種類, '字詞')
        self.assertEqual(聽拍.語言腔口.語言腔口, '閩南語')
        self.assertEqual(聽拍.著作所在地.著作所在地, '花蓮')
        self.assertEqual(聽拍.著作年.著作年, '2014')
        self.assertEqual(聽拍.屬性.count(), 0)
        self.assertEqual(json.loads(聽拍.聽拍資料), [
            {'語者': '阿宏', '內容': 'li1', '開始時間': 0.0, '結束時間': 1.2},
            {'語者': '阿莉', '內容': 'ho2', '開始時間': 1.2, '結束時間': 2.0},
        ])

    def 加句(self, 原本聽拍):
        原來聽拍資料數 = 聽拍表.objects.all().count()
        原來聽拍校對數 = 聽拍校對表.objects.all().count()
        聽拍 = 原本聽拍.校對做(self.對應資料句內容)
        self.assertEqual(聽拍表.objects.all().count(), 原來聽拍資料數 + 1)
        self.assertEqual(聽拍校對表.objects.all().count(), 原來聽拍校對數 + 1)
        self.assertIsInstance(原本聽拍.聽拍校對.get(新聽拍=聽拍), 聽拍校對表)
        self.assertEqual(原本聽拍.聽拍校對.get(新聽拍=聽拍).新聽拍, 聽拍)
        self.assertEqual(聽拍.收錄者.名, 'Dr. Pigu')
        self.assertEqual(聽拍.收錄者.屬性內容(), {'出世年': '1990', '出世地': '花蓮人'})
        self.assertEqual(聽拍.來源.名, '鄉民')
        self.assertEqual(聽拍.來源.屬性內容(), {'出世年': '1950', '出世地': '臺灣'})
        self.assertEqual(聽拍.版權.版權, '袂使公開')
        self.assertEqual(聽拍.種類.種類, '語句')
        self.assertEqual(聽拍.語言腔口.語言腔口, '四縣話')
        self.assertEqual(聽拍.著作所在地.著作所在地, '臺灣')
        self.assertEqual(聽拍.著作年.著作年, '195x')
        self.assertEqual(聽拍.屬性.count(), 0)
        self.assertEqual(json.loads(聽拍.聽拍資料),
                         [
            {'內容': '請問車頭按怎行？'},
            {'內容': '直直行就到矣。'},
        ]
        )

    def test_是校對資料(self):
        第一層詞 = self.原本資料表.加資料(self.原本資料詞內容)
        self.assertFalse(第一層詞.是校對後的資料())
        第二層詞 = 第一層詞.校對做(self.對應資料詞內容)
        self.assertFalse(第一層詞.是校對後的資料())
        self.assertTrue(第二層詞.是校對後的資料())

        第一層句 = self.原本資料表.加資料(self.原本資料句內容)
        self.assertFalse(第一層句.是校對後的資料())
        第二層句 = 第一層句.校對做(self.對應資料句內容)
        self.assertFalse(第一層句.是校對後的資料())
        self.assertTrue(第二層句.是校對後的資料())

    def test_語料會使校對兩擺以上(self):
        原來聽拍資料數 = 聽拍表.objects.all().count()
        原來聽拍校對數 = 聽拍校對表.objects.all().count()

        第一層詞 = self.原本資料表.加資料(self.原本資料詞內容)
        第一層詞.校對做(self.對應資料詞內容)
        第一層詞.校對做(self.對應資料詞內容)
        self.assertEqual(聽拍表.objects.all().count(), 原來聽拍資料數 + 3)
        self.assertEqual(聽拍校對表.objects.all().count(), 原來聽拍校對數 + 2)

        第一層句 = self.原本資料表.加資料(self.原本資料句內容)
        第一層句.校對做(self.對應資料句內容)
        第一層句.校對做(self.對應資料句內容)
        self.assertEqual(聽拍表.objects.all().count(), 原來聽拍資料數 + 6)
        self.assertEqual(聽拍校對表.objects.all().count(), 原來聽拍校對數 + 4)

    def test_語料會使三層以上(self):
        原來聽拍資料數 = 聽拍表.objects.all().count()
        原來聽拍校對數 = 聽拍校對表.objects.all().count()

        第一層詞 = self.原本資料表.加資料(self.原本資料詞內容)
        第二層詞 = 第一層詞.校對做(self.對應資料詞內容)
        第二層詞.校對做(self.對應資料詞內容)
        self.assertEqual(聽拍表.objects.all().count(), 原來聽拍資料數 + 3)
        self.assertEqual(聽拍校對表.objects.all().count(), 原來聽拍校對數 + 2)

        第一層句 = self.原本資料表.加資料(self.原本資料句內容)
        第二層句 = 第一層句.校對做(self.對應資料句內容)
        第二層句.校對做(self.對應資料句內容)
        self.assertEqual(聽拍表.objects.all().count(), 原來聽拍資料數 + 6)
        self.assertEqual(聽拍校對表.objects.all().count(), 原來聽拍校對數 + 4)
