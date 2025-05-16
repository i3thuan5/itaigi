# -*- coding: utf-8 -*-
from django.test import TestCase
import json


from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語平臺.使用者模型 import 使用者表


class 看來源內容試驗(TestCase):

    def test_一般來源(self):
        來源內容 = {"名": '鄉民', '出世年': '1950', '出世地': '臺灣', }
        使用者 = 使用者表.加使用者('sui2@pigu.tw', 來源內容,)
# 		前端輸入
        回應 = self.client.get('/平臺項目來源/看內容', {'來源編號': 使用者.編號()})
# 		前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertEqual(回應資料, {
            '名': '鄉民',
            '屬性內容': {'出世年': '1950', '出世地': '臺灣'},
            'email': 'sui2@pigu.tw',
        })
# 		後端檢查
        self.assertEqual(使用者.來源.編號(), 使用者.編號())

    def test_一般來源無使用者(self):
        鄉民 = 來源表. 加來源({"名": '鄉民', '出世年': '1950', '出世地': '臺灣', })
# 		前端輸入
        回應 = self.client.get('/平臺項目來源/看內容', {'來源編號': 鄉民.編號()})
# 		前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertEqual(回應資料, {
            '名': '鄉民',
            '屬性內容': {'出世年': '1950', '出世地': '臺灣', },
        })

    def test_無來源(self):
        # 		前端輸入
        回應 = self.client.get('/平臺項目來源/看內容', {'來源編號': 來源表.objects.count() + 10})
# 		前端回傳結果
        self.assertEqual(回應.status_code, 400)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertEqual(回應資料, {
            '錯誤': '這不是合法的來源編號'
        })

    def test_沒有來源編號參數(self):
        # 		前端輸入
        回應 = self.client.get('/平臺項目來源/看內容')
# 		前端回傳結果
        self.assertEqual(回應.status_code, 400)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertEqual(回應資料, {
            '錯誤': '沒有來源編號的參數'
        })
