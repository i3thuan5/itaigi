# -*- coding: utf-8 -*-
import json

from django.core.exceptions import ValidationError
from django.test import TestCase
from 試驗.加資料.加資料試驗 import 加資料試驗
from 臺灣言語資料庫.資料模型 import 文本表


class 加文本資料試驗(TestCase, 加資料試驗):

    def setUp(self):
        self.加初始資料佮設定變數()
        self.資料表 = 文本表
        self.詞內容.update({
            '文本資料': '媠',
        })
        self.句內容.update({
            '文本資料': '伊誠媠。',
        })

    def test_加詞(self):
        super(加文本資料試驗, self).test_加詞()
        self.assertEqual(self.資料.文本資料, '媠')

    def test_加句(self):
        super(加文本資料試驗, self).test_加句()
        self.assertEqual(self.資料.文本資料, '伊誠媠。')

    def test_無資料(self):
        self.詞內容.pop('文本資料')
        self.assertRaises(KeyError, super(加文本資料試驗, self).test_加詞)
        self.assertEqual(self.資料表.objects.all().count(), 0)
        self.句內容.pop('文本資料')
        self.assertRaises(KeyError, super(加文本資料試驗, self).test_加句)
        self.assertEqual(self.資料表.objects.all().count(), 0)

    def test_資料毋是字串(self):
        self.句內容['文本資料'] = 2005
        with self.assertRaises(ValueError):
            self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)
        self.句內容['文本資料'] = None
        with self.assertRaises(ValueError):
            self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)
        self.句內容['文本資料'] = [' 南投縣噶哈巫文教協會', '眉溪四庄重建工作站']
        with self.assertRaises(ValueError):
            self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)

    def test_資料是空的(self):
        self.句內容['文本資料'] = ''
        self.assertRaises(ValidationError, self.資料表.加資料, self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)

    def test_音標資料欄位(self):
        self.句內容.update({
            '音標資料': 'i1 tsiann5 sui2 .',
            '屬性': {},
        })
        self.資料 = self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料.音標資料, 'i1 tsiann5 sui2 .')
        self.assertEqual(self.資料.屬性.count(), 0)

    def test_屬性的音標愛存去音標資料(self):
        self.句內容.update({
            '屬性': {'音標': 'i1 tsiann5 sui2 .', },
        })
        self.資料 = self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料.音標資料, 'i1 tsiann5 sui2 .')
        self.assertEqual(self.資料.屬性.count(), 0)

    def test_字串的屬性音標愛存去音標資料(self):
        self.句內容.update({
            '屬性': json.dumps({'音標': 'i1 tsiann5 sui2 .', }),
        })
        self.資料 = self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料.音標資料, 'i1 tsiann5 sui2 .')
        self.assertEqual(self.資料.屬性.count(), 0)
