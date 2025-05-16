# -*- coding: utf-8 -*-
import codecs
from django.test import TestCase
import io
import json
from os.path import abspath, dirname, join
import wave


from 試驗.加資料.加資料試驗 import 加資料試驗
from 臺灣言語資料庫.資料模型 import 影音表


class 加影音資料試驗(TestCase, 加資料試驗):

    def setUp(self):
        self.加初始資料佮設定變數()
        self.資料表 = 影音表
        self.詞檔案 = io.BytesIO()
        音檔 = wave.open(self.詞檔案, 'wb')
        音檔.setnchannels(1)
        音檔.setframerate(16000)
        音檔.setsampwidth(2)
        音檔.writeframesraw(b'0' * 100)
        音檔.close()
        self.句檔案 = io.BytesIO()
        音檔 = wave.open(self.句檔案, 'wb')
        音檔.setnchannels(1)
        音檔.setframerate(16000)
        音檔.setsampwidth(2)
        音檔.writeframesraw(b'sui2' * 80000)
        音檔.close()
        self.詞內容.update({
            '影音資料': self.詞檔案,
        })
        self.句內容.update({
            '影音資料': self.句檔案,
        })

    def tearDown(self):
        self.詞檔案.close()
        self.句檔案.close()

    def test_加詞(self):
        super(加影音資料試驗, self).test_加詞()
        self.資料.影音資料.open()
        self.assertEqual(self.資料.影音資料.read(), self.詞檔案.getvalue())
        self.資料.影音資料.close()
# 		self.assertEqual(self.資料.網頁影音資料,)

    def test_加句(self):
        super(加影音資料試驗, self).test_加句()
        self.資料.影音資料.open()
        self.assertEqual(self.資料.影音資料.read(), self.句檔案.getvalue())
        self.資料.影音資料.close()
# 		self.assertEqual(self.資料.網頁影音資料,)

    def test_無資料(self):
        self.詞內容.pop('影音資料')
        self.assertRaises(KeyError, super(加影音資料試驗, self).test_加詞)
        self.assertEqual(self.資料表.objects.all().count(), 0)
        self.句內容.pop('影音資料')
        self.assertRaises(KeyError, super(加影音資料試驗, self).test_加句)
        self.assertEqual(self.資料表.objects.all().count(), 0)
    # 	照django.File傳AttributeError

    def test_影音資料毋是檔案(self):
        self.句內容['影音資料'] = 2015
        with self.assertRaises(ValueError):
            self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)
        self.句內容['影音資料'] = None
        with self.assertRaises(ValueError):
            self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)
        self.句內容['影音資料'] = codecs.encode('牛睏山部落的織布機課程、守城社區的母語課程')
        with self.assertRaises(ValueError):
            self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)
        self.句內容['影音資料'] = '牛睏山部落的織布機課程、守城社區的母語課程'
        with self.assertRaises(ValueError):
            self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)
    # 檔案無法度轉json字串，所以這愛改做無檔案的error

    def test_規個內容用字串(self):
        self.詞內容.pop('影音資料')
        self.詞內容 = json.dumps(self.詞內容)
        self.assertRaises(KeyError, super(加影音資料試驗, self).test_加詞)
        self.assertEqual(self.資料表.objects.all().count(), 0)
        self.句內容.pop('影音資料')
        self.句內容 = json.dumps(self.句內容)
        self.assertRaises(KeyError, super(加影音資料試驗, self).test_加句)
        self.assertEqual(self.資料表.objects.all().count(), 0)

    def test_傳檔案所在(self):
        檔案所在 = join(dirname(abspath(__file__)), 'audio/08310.mp3')
        self.詞內容.pop('影音資料')
        self.詞內容['影音所在'] = 檔案所在
        super(加影音資料試驗, self).test_加詞()
        with open(檔案所在, 'rb') as 聲音檔案:
            self.assertEqual(self.資料.影音資料.read(), 聲音檔案.read())

    def test_傳網址所在(self):
        網址所在 = 'http://t.moedict.tw/08310.mp3'
        self.詞內容.pop('影音資料')
        self.詞內容['影音所在'] = 網址所在
        super(加影音資料試驗, self).test_加詞()
        檔案所在 = join(dirname(abspath(__file__)), 'audio/08310.mp3')
        with open(檔案所在, 'rb') as 聲音檔案:
            self.assertEqual(self.資料.影音資料.read(), 聲音檔案.read())

    def test_傳網址所在無協定(self):
        網址所在 = 't.moedict.tw/08310.mp3'
        self.詞內容.pop('影音資料')
        self.詞內容['影音所在'] = 網址所在
        super(加影音資料試驗, self).test_加詞()
        檔案所在 = join(dirname(abspath(__file__)), 'audio/08310.mp3')
        with open(檔案所在, 'rb') as 聲音檔案:
            self.assertEqual(self.資料.影音資料.read(), 聲音檔案.read())

    def test_袂使傳資料閣傳所在(self):
        網址所在 = join(dirname(abspath(__file__)), 'audio/08310.mp3')
        self.詞內容['影音所在'] = 網址所在
        with self.assertRaises(ValueError):
            super(加影音資料試驗, self).test_加詞()
