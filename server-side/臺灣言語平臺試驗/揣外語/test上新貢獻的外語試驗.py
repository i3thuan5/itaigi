# -*- coding: utf-8 -*-
from django.urls.base import resolve
from django.test import TestCase


from 臺灣言語平臺.項目模型 import 平臺項目表
from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語平臺.介面.揣外語請教條 import 揣上新貢獻的外語請教條


class 上新貢獻的外語試驗(TestCase):

    def setUp(self):
        self.鄉民 = 來源表. 加來源({"名": '鄉民', '出世年': '1950', '出世地': '臺灣', })
        self.外語內容 = {
            '外語資料': '水母',
        }

    def test_對應函式(self):
        對應 = resolve('/平臺項目列表/揣上新貢獻的外語')
        self.assertEqual(對應.func, 揣上新貢獻的外語請教條)

    def test_無外語物件(self):
        回應 = self.client.get('/平臺項目列表/揣上新貢獻的外語')
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['列表'], [])

    def test_外語無物件(self):
        平臺項目表.加外語資料(self.外語內容).編號()
#         前端輸入
        回應 = self.client.get('/平臺項目列表/揣上新貢獻的外語')
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['列表'], [])

    def test_外語有文本無校對仝款袂使出現(self):
        水母編號 = 平臺項目表.加外語資料(self.外語內容).編號()
        䖳文本內容 = {
            '文本資料': '䖳',
        }
        平臺項目表.外語翻母語(水母編號, 䖳文本內容)
#         前端輸入
        回應 = self.client.get('/平臺項目列表/揣上新貢獻的外語')
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['列表'], [])

    def test_外語有建議文本就愛出現(self):
        水母編號 = 平臺項目表.加外語資料(self.外語內容).編號()
        䖳文本內容 = {
            '文本資料': '䖳',
        }
        文本 = 平臺項目表.外語翻母語(水母編號, 䖳文本內容)
        新文本 = 平臺項目表._校對母語文本(文本.編號(), {
            '文本資料': '䖳',
            '屬性': {'音標': 'the7'}
        })
        新文本.設為推薦用字()
#         前端輸入
        回應 = self.client.get('/平臺項目列表/揣上新貢獻的外語')
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['列表'], [{
            '外語項目編號': str(水母編號),
            '外語資料': '水母',
        }])

    def test_外語有建議是著的愛出現(self):
        水母編號 = 平臺項目表.加外語資料(self.外語內容).編號()
        䖳文本內容 = {
            '文本資料': '䖳',
        }
        文本 = 平臺項目表.外語翻母語(水母編號, 䖳文本內容)
        文本.設為推薦用字()
#         前端輸入
        回應 = self.client.get('/平臺項目列表/揣上新貢獻的外語')
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['列表'], [{
            '外語項目編號': str(水母編號),
            '外語資料': '水母',
        }])

    def test_外語後貢獻的排頭前(self):
        水母編號 = 平臺項目表.加外語資料({'外語資料': '水母'}).編號()
        水編號 = 平臺項目表.加外語資料({'外語資料': '水'}).編號()
        文本 = 平臺項目表.外語翻母語(水編號, {'文本資料': '水'})
        新文本 = 平臺項目表._校對母語文本(文本.編號(), {
            '文本資料': '水',
            '屬性': {'音標': 'tsui2'}
        })
        新文本.設為推薦用字()
        文本 = 平臺項目表.外語翻母語(水母編號, {'文本資料': '䖳'})
        新文本 = 平臺項目表._校對母語文本(文本.編號(), {
            '文本資料': '䖳',
            '屬性': {'音標': 'the7'}
        })
        新文本.設為推薦用字()
#         前端輸入
        回應 = self.client.get('/平臺項目列表/揣上新貢獻的外語')
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['列表'], [
            {
                '外語項目編號': str(水母編號),
                '外語資料': '水母',
            },
            {
                '外語項目編號': str(水編號),
                '外語資料': '水',
            },
        ])
