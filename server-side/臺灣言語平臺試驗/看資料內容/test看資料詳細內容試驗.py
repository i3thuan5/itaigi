# -*- coding: utf-8 -*-
import io
import json
import wave

from django.urls.base import resolve
from django.test import TestCase


from 臺灣言語平臺.項目模型 import 平臺項目表
from 臺灣言語平臺.介面.看資料內容 import 看資料詳細內容


class 看資料詳細內容試驗(TestCase):

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

    def test_有對應函式(self):
        對應 = resolve('/平臺項目/看詳細內容')
        self.assertEqual(對應.func, 看資料詳細內容)

    def test_資料外語(self):
        外語項目編號 = 平臺項目表.加外語資料(self.外語內容).編號()
# 		前端輸入
        回應 = self.client.get('/平臺項目/看詳細內容', {'平臺項目編號': 外語項目編號})
# 		前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertIn('收錄者', 回應資料)
        self.assertIn('來源', 回應資料)
        self.assertIn('收錄時間', 回應資料)
        self.assertIn('種類', 回應資料)
        self.assertIn('版權', 回應資料)
        self.assertIn('著作所在地', 回應資料)
        self.assertIn('著作年', 回應資料)
        self.assertIn('屬性內容', 回應資料)

    def test_資料影音(self):
        外語項目編號 = 平臺項目表.加外語資料(self.外語內容).編號()
        影音項目編號 = 平臺項目表.外語錄母語(外語項目編號, self.影音內容).編號()
# 		前端輸入
        回應 = self.client.get('/平臺項目/看詳細內容', {'平臺項目編號': 影音項目編號})
# 		前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertIn('收錄者', 回應資料)
        self.assertIn('來源', 回應資料)
        self.assertIn('收錄時間', 回應資料)
        self.assertIn('種類', 回應資料)
        self.assertIn('版權', 回應資料)
        self.assertIn('著作所在地', 回應資料)
        self.assertIn('著作年', 回應資料)
        self.assertIn('屬性內容', 回應資料)

    def test_資料文本(self):
        外語項目編號 = 平臺項目表.加外語資料(self.外語內容).編號()
        影音項目編號 = 平臺項目表.外語錄母語(外語項目編號, self.影音內容).編號()
        文本項目編號 = 平臺項目表.影音寫文本(影音項目編號, self.文本內容).編號()
# 		前端輸入
        回應 = self.client.get('/平臺項目/看詳細內容', {'平臺項目編號': 文本項目編號})
# 		前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertIn('收錄者', 回應資料)
        self.assertIn('來源', 回應資料)
        self.assertIn('收錄時間', 回應資料)
        self.assertIn('種類', 回應資料)
        self.assertIn('版權', 回應資料)
        self.assertIn('著作所在地', 回應資料)
        self.assertIn('著作年', 回應資料)
        self.assertIn('屬性內容', 回應資料)

    def test_資料攏無(self):
        # 		前端輸入
        回應 = self.client.get('/平臺項目/看詳細內容',
                             {'平臺項目編號': 平臺項目表.objects.all().count() + 1})
# 		前端回傳結果
        self.assertEqual(回應.status_code, 400)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertEqual(回應資料, {'錯誤': '這不是合法平臺項目的編號'})

    def test_無傳參數(self):
        # 		前端輸入
        回應 = self.client.get('/平臺項目/看詳細內容')
# 		前端回傳結果
        self.assertEqual(回應.status_code, 400)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertEqual(回應資料, {'錯誤': '沒有平臺項目的編號'})
