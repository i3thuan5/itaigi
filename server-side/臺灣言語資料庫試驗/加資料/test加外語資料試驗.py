# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.test import TestCase
import json
from 試驗.加資料.加資料試驗 import 加資料試驗
from 臺灣言語資料庫.資料模型 import 外語表


class 加外語資料試驗(TestCase, 加資料試驗):

    def setUp(self):
        self.加初始資料佮設定變數()
        self.資料表 = 外語表
        self.詞內容.update({
            '外語語言': '華語',
            '外語資料': '漂亮',
        })
        self.句內容.update({
            '外語語言': '英語',
            '外語資料': 'She is beautiful.',
        })

    def test_加詞(self):
        super(加外語資料試驗, self).test_加詞()
        self.assertEqual(self.資料.外語語言, self.華語)
        self.assertEqual(self.資料.外語資料, '漂亮')

    def test_加句(self):
        super(加外語資料試驗, self).test_加句()
        self.assertEqual(self.資料.外語語言, self.英語)
        self.assertEqual(self.資料.外語資料, 'She is beautiful.')

    def test_外語語言舊編號(self):
        self.詞內容['外語語言'] = self.華語.pk
        super(加外語資料試驗, self).test_加詞()
        self.assertEqual(self.資料.外語語言, self.華語)
        self.assertEqual(self.資料.外語資料, '漂亮')
        self.句內容['外語語言'] = self.英語.pk
        super(加外語資料試驗, self).test_加句()
        self.assertEqual(self.資料.外語語言, self.英語)
        self.assertEqual(self.資料.外語資料, 'She is beautiful.')

    def test_外語語言新字串(self):
        self.詞內容['外語語言'] = '埔里噶哈巫'
        super(加外語資料試驗, self).test_加詞()
        self.assertEqual(self.資料.外語語言.語言腔口, '埔里噶哈巫')
        self.assertEqual(self.資料.外語資料, '漂亮')
        self.句內容['外語語言'] = '日語'
        super(加外語資料試驗, self).test_加句()
        self.assertEqual(self.資料.外語語言.語言腔口, '日語')
        self.assertEqual(self.資料.外語資料, 'She is beautiful.')

    def test_外語語言新編號(self):
        self.詞內容['外語語言'] = 1115
        self.assertRaises(ObjectDoesNotExist, super(加外語資料試驗, self).test_加詞)
        self.assertEqual(self.資料表.objects.all().count(), 0)
        self.句內容['外語語言'] = 1231
        self.assertRaises(ObjectDoesNotExist, super(加外語資料試驗, self).test_加句)
        self.assertEqual(self.資料表.objects.all().count(), 0)

    def test_外語語言毋是數字佮字串(self):
        self.詞內容['外語語言'] = [1115]
        with self.assertRaises(ValueError):
            super(加外語資料試驗, self).test_加詞()
        self.assertEqual(self.資料表.objects.all().count(), 0)
        self.句內容['外語語言'] = 1231.23
        with self.assertRaises(ValueError):
            super(加外語資料試驗, self).test_加詞()
        self.assertEqual(self.資料表.objects.all().count(), 0)

    def test_無語言(self):
        self.詞內容.pop('外語語言')
        self.assertRaises(KeyError, super(加外語資料試驗, self).test_加詞)
        self.assertEqual(self.資料表.objects.all().count(), 0)
        self.句內容.pop('外語語言')
        self.assertRaises(KeyError, super(加外語資料試驗, self).test_加句)
        self.assertEqual(self.資料表.objects.all().count(), 0)

    def test_無資料(self):
        self.詞內容.pop('外語資料')
        self.assertRaises(KeyError, super(加外語資料試驗, self).test_加詞)
        self.assertEqual(self.資料表.objects.all().count(), 0)
        self.句內容.pop('外語資料')
        self.assertRaises(KeyError, super(加外語資料試驗, self).test_加句)
        self.assertEqual(self.資料表.objects.all().count(), 0)

    def test_毋是字串(self):
        self.詞內容['外語資料'] = 1228
        with self.assertRaises(ValueError):
            super(加外語資料試驗, self).test_加詞()
        self.assertEqual(self.資料表.objects.all().count(), 0)
        self.句內容['外語資料'] = ['沒辦法']
        with self.assertRaises(ValueError):
            super(加外語資料試驗, self).test_加詞()
        self.assertEqual(self.資料表.objects.all().count(), 0)
        self.詞內容['外語資料'] = None
        with self.assertRaises(ValueError):
            super(加外語資料試驗, self).test_加詞()
        self.assertEqual(self.資料表.objects.all().count(), 0)
        self.句內容['外語資料'] = {}
        with self.assertRaises(ValueError):
            super(加外語資料試驗, self).test_加詞()
        self.assertEqual(self.資料表.objects.all().count(), 0)

    def test_資料是空的(self):
        self.詞內容['外語資料'] = ''
        self.assertRaises(ValidationError, super(加外語資料試驗, self).test_加詞)
        self.assertEqual(self.資料表.objects.all().count(), 0)

    def test_屬性是json字串(self):
        外語 = 外語表.加資料({
            '著作年': '2014',
            '外語資料': '漂亮',
            '種類': '字詞',
            '收錄者': self.詞內容['收錄者'],
            '著作所在地': '花蓮',
            '語言腔口': '閩南語',
            '版權': '會使公開',
            '外語語言': '華語',
            '來源':
            '{"\\u8077\\u696d": "\\u5b78\\u751f", "\\u540d": "\\u963f\\u5aa0"}',
            '屬性':
            '{"\\u5b57\\u6578": "2", "\\u8a5e\\u6027": "\\u5f62\\u5bb9\\u8a5e"}'
        })
        self.assertEqual(外語.屬性.count(), 2)
        self.assertEqual(json.loads(外語.屬性.get(分類='詞性').性質), '形容詞')
        self.assertEqual(json.loads(外語.屬性.get(分類='字數').性質), '2')
