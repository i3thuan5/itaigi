# -*- coding: utf-8 -*-
import json

from django.urls.base import resolve
from django.test import TestCase
from 臺灣言語平臺.項目模型 import 平臺項目表
from 臺灣言語平臺.介面.揣外語請教條 import 揣按呢講外語請教條


class 揣按呢講外語試驗(TestCase):

    def test_有對應函式(self):
        對應 = resolve('/平臺項目列表/揣按呢講列表')
        self.assertEqual(對應.func, 揣按呢講外語請教條)

    def test_揣無(self):
        # 		前端輸入
        回應 = self.client.get('/平臺項目列表/揣按呢講列表', {
            '關鍵字': '水母'
        })
# 		前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料, {
            '列表': [],
        })

    def test_文本無建議用字當做揣無(self):
        水母編號 = self.資料庫加外語('水母')
        平臺項目表.外語翻母語(水母編號, {
            '文本資料': '䖳',
        })
#         前端輸入
        回應 = self.client.get('/平臺項目列表/揣按呢講列表', {
            '關鍵字': '䖳'
        })
#         前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料, {
            '列表': [],
        })

    def test_文本有建議用字就揣會著(self):
        水母編號 = self.資料庫加外語('水母')
        文本 = 平臺項目表.外語翻母語(水母編號, {
            '文本資料': '䖳',
        })
        文本.設為推薦用字()
#         前端輸入
        回應 = self.client.get('/平臺項目列表/揣按呢講列表', {
            '關鍵字': '䖳'
        })
#         前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['列表'], [{
            '外語項目編號': str(水母編號),
            '外語資料': '水母'
        }])

    def test_文本有閣校對過就揣會著(self):
        水母編號 = self.資料庫加外語('水母')
        文本 = 平臺項目表.外語翻母語(水母編號, {
            '文本資料': 'the7',
        })
        新文本 = 平臺項目表._校對母語文本(文本.編號(), {
            '文本資料': '䖳',
            '屬性': {'音標': 'the7'}
        })
        新文本.設為推薦用字()
#         前端輸入
        回應 = self.client.get('/平臺項目列表/揣按呢講列表', {
            '關鍵字': '䖳'
        })
#         前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['列表'], [{
            '外語項目編號': str(水母編號),
            '外語資料': '水母'
        }])

    def test_文本有兩組建議用字(self):
        水母編號 = self.資料庫加外語('水母')
        文本 = 平臺項目表.外語翻母語(水母編號, {
            '文本資料': '䖳',
        })
        文本.設為推薦用字()
        小九編號 = self.資料庫加外語('小九')
        文本 = 平臺項目表.外語翻母語(小九編號, {
            '文本資料': '䖳',
        })
        文本.設為推薦用字()
#         前端輸入
        回應 = self.client.get('/平臺項目列表/揣按呢講列表', {
            '關鍵字': '䖳'
        })
#         前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(len(回應資料['列表']), 2)

    def test_無傳關鍵字(self):
        # 		前端輸入
        回應 = self.client.get('/平臺項目列表/揣按呢講列表', {
            # 				'關鍵字':'水母'
        })
# 		前端回傳結果
        self.assertEqual(回應.status_code, 400)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertEqual(回應資料, {'錯誤': '無傳關鍵字'})

    def 資料庫加外語(self, 外語詞):
        return 平臺項目表.加外語資料(
            {
                '外語資料': 外語詞,
            }
        ).編號()
