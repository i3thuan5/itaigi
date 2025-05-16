# -*- coding: utf-8 -*-
from django.test import TestCase
from 試驗.加關係.加關係試驗 import 加關係試驗
import json
from 臺灣言語資料庫.資料模型 import 影音表
from 臺灣言語資料庫.資料模型 import 文本表
from 臺灣言語資料庫.關係模型 import 影音文本表


class 加影音文本試驗(加關係試驗, TestCase):

    def setUp(self):
        self.加初始資料()
        self.原本資料表 = 影音表
        self.原本資料詞內容 = {
            '收錄者': json.dumps({'名': '鄉民', '出世年': '1950', '出世地': '臺灣'}),
            '來源': json.dumps({'名': 'Dr. Pigu', '出世年': '1990', '出世地': '花蓮人'}),
            '版權': '會使公開',
            '種類': '字詞',
            '語言腔口': '閩南語',
            '著作所在地': '花蓮',
            '著作年': '2014',
            '影音資料': self.詞檔案,
        }
        self.原本資料句內容 = {
            '收錄者': json.dumps({'名': 'Dr. Pigu', '出世年': '1990', '出世地': '花蓮人'}),
            '來源': json.dumps({'名': '鄉民', '出世年': '1950', '出世地': '臺灣'}),
            '版權': '袂使公開',
            '種類': '語句',
            '語言腔口': '四縣話',
            '著作所在地': '臺灣',
            '著作年': '195x',
            '影音資料': self.句檔案,
        }
        self.對應資料詞內容 = {
            '收錄者': json.dumps({'名': '鄉民', '出世年': '1950', '出世地': '臺灣'}),
            '來源': json.dumps({'名': 'Dr. Pigu', '出世年': '1990', '出世地': '花蓮人'}),
            '版權': '會使公開',
            '種類': '字詞',
            '語言腔口': '閩南語',
            '著作所在地': '花蓮',
            '著作年': '2014',
            '文本資料': '媠',
        }
        self.對應資料句內容 = {
            '收錄者': json.dumps({'名': 'Dr. Pigu', '出世年': '1990', '出世地': '花蓮人'}),
            '來源': json.dumps({'名': '鄉民', '出世年': '1950', '出世地': '臺灣'}),
            '版權': '袂使公開',
            '種類': '語句',
            '語言腔口': '四縣話',
            '著作所在地': '臺灣',
            '著作年': '195x',
            '文本資料': '伊誠媠。',
        }

    def 加詞(self, 影音):
        原來影音資料數 = 影音表.objects.all().count()
        原來文本資料數 = 文本表.objects.all().count()
        原來影音文本數 = 影音文本表.objects.all().count()
        文本 = 影音.寫文本(self.對應資料詞內容)
        self.assertEqual(影音表.objects.all().count(), 原來影音資料數)
        self.assertEqual(文本表.objects.all().count(), 原來文本資料數 + 1)
        self.assertEqual(影音文本表.objects.all().count(), 原來影音文本數 + 1)
        self.assertIsInstance(影音.影音文本.get(文本=文本), 影音文本表)
        self.assertEqual(影音.影音文本.get(文本=文本).文本, 文本)
        self.assertEqual(文本.收錄者.名, '鄉民')
        self.assertEqual(文本.收錄者.屬性內容(), {'出世年': '1950', '出世地': '臺灣'})
        self.assertEqual(文本.來源.名, 'Dr. Pigu')
        self.assertEqual(文本.來源.屬性內容(), {'出世年': '1990', '出世地': '花蓮人'})
        self.assertEqual(文本.版權.版權, '會使公開')
        self.assertEqual(文本.種類.種類, '字詞')
        self.assertEqual(文本.語言腔口.語言腔口, '閩南語')
        self.assertEqual(文本.著作所在地.著作所在地, '花蓮')
        self.assertEqual(文本.著作年.著作年, '2014')
        self.assertEqual(文本.屬性.count(), 0)
        self.assertEqual(文本.文本資料, '媠')

    def 加句(self, 影音):
        原來影音資料數 = 影音表.objects.all().count()
        原來文本資料數 = 文本表.objects.all().count()
        原來影音文本數 = 影音文本表.objects.all().count()
        文本 = 影音.寫文本(self.對應資料句內容)
        self.assertEqual(影音表.objects.all().count(), 原來影音資料數)
        self.assertEqual(文本表.objects.all().count(), 原來文本資料數 + 1)
        self.assertEqual(影音文本表.objects.all().count(), 原來影音文本數 + 1)
        self.assertIsInstance(影音.影音文本.get(文本=文本), 影音文本表)
        self.assertEqual(影音.影音文本.get(文本=文本).文本, 文本)
        self.assertEqual(文本.收錄者.名, 'Dr. Pigu')
        self.assertEqual(文本.收錄者.屬性內容(), {'出世年': '1990', '出世地': '花蓮人'})
        self.assertEqual(文本.來源.名, '鄉民')
        self.assertEqual(文本.來源.屬性內容(), {'出世年': '1950', '出世地': '臺灣'})
        self.assertEqual(文本.版權.版權, '袂使公開')
        self.assertEqual(文本.種類.種類, '語句')
        self.assertEqual(文本.語言腔口.語言腔口, '四縣話')
        self.assertEqual(文本.著作所在地.著作所在地, '臺灣')
        self.assertEqual(文本.著作年.著作年, '195x')
        self.assertEqual(文本.屬性.count(), 0)
        self.assertEqual(文本.文本資料, '伊誠媠。')
