# -*- coding: utf-8 -*-
from django.test import TestCase
import io
import wave
from 臺灣言語平臺.項目模型 import 平臺項目表
from django.core.exceptions import ObjectDoesNotExist


class 項目模型試驗(TestCase):

    def setUp(self):
        self.外語內容 = {
            '外語資料': '水母',
        }

        檔案 = io.BytesIO()
        with wave.open(檔案, 'wb') as 音檔:
            音檔.setnchannels(1)
            音檔.setframerate(16000)
            音檔.setsampwidth(2)
            音檔.writeframesraw(b'sui2' * 20)
        檔案.seek(0)
        檔案.name = '試驗音檔'
        self.影音內容 = {
            '影音資料': 檔案,
        }
        self.文本內容 = {
            '文本資料': '䖳',
        }

    def tearDown(self):
        pass

    def test_編號(self):
        平臺項目 = 平臺項目表.加外語資料(self.外語內容)
        self.assertEqual(平臺項目.編號(), 平臺項目.pk,)

    def test_揣編號(self):
        平臺項目 = 平臺項目表.加外語資料(self.外語內容)
        self.assertEqual(平臺項目表.揣編號(平臺項目.編號()), 平臺項目)

    def test_資料外語(self):
        外語項目 = 平臺項目表.加外語資料(self.外語內容)
        self.assertEqual(外語項目.資料(), 外語項目.外語)

    def test_資料影音(self):
        外語項目 = 平臺項目表.加外語資料(self.外語內容)
        影音項目 = 平臺項目表.外語錄母語(外語項目.編號(), self.影音內容)
        self.assertEqual(影音項目.資料(), 影音項目.影音)

    def test_資料文本(self):
        外語項目 = 平臺項目表.加外語資料(self.外語內容)
        影音項目 = 平臺項目表.外語錄母語(外語項目.編號(), self.影音內容)
        文本項目 = 平臺項目表.影音寫文本(影音項目.編號(), self.文本內容)
        self.assertEqual(文本項目.資料(), 文本項目.文本)

    def test_資料攏無(self):
        攏無 = 平臺項目表.objects.create()
        self.assertRaises(RuntimeError, 攏無.資料)

    def test_資料袂使超過一个(self):
        濟个項目 = 平臺項目表.加外語資料(self.外語內容)
        影音項目 = 平臺項目表.外語錄母語(濟个項目.編號(), self.影音內容)
        濟个項目.影音 = 影音項目.影音
        self.assertRaises(RuntimeError, 濟个項目.資料)

    def test_找外語資料揣有(self):
        外語項目 = 平臺項目表.加外語資料(self.外語內容)
        找到的外語項目 = 平臺項目表._找外語資料(self.外語內容)
        self.assertEqual(外語項目, 找到的外語項目)

    def test_找外語資料種類表揣無(self):
        平臺項目表.加外語資料(self.外語內容)
        self.外語內容['種類'] = '語句'
        self.assertRaises(ObjectDoesNotExist, 平臺項目表._找外語資料, self.外語內容)

    def test_找外語資料語言腔口揣無(self):
        平臺項目表.加外語資料(self.外語內容)
        self.外語內容['語言腔口'] = '噶哈巫'
        self.assertRaises(ObjectDoesNotExist, 平臺項目表._找外語資料, self.外語內容)

    def test_找外語資料外語語言揣無(self):
        平臺項目表.加外語資料(self.外語內容)
        self.外語內容['外語語言'] = '噶哈巫'
        self.assertRaises(ObjectDoesNotExist, 平臺項目表._找外語資料, self.外語內容)
