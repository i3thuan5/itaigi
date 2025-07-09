# -*- coding: utf-8 -*-
import json

from django.urls.base import resolve
from django.test import TestCase
from 臺灣言語平臺.項目模型 import 平臺項目表
from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語平臺.介面.揣外語請教條 import 揣外語請教條


class 揣外語試驗(TestCase):

    def setUp(self):
        self.鄉民 = 來源表. 加來源({"名": '鄉民', '出世年': '1950', '出世地': '臺灣', })

    def test_有對應函式(self):
        對應 = resolve('/平臺項目列表/揣列表')
        self.assertEqual(對應.func, 揣外語請教條)

    def test_揣無(self):
        # 		前端輸入
        回應 = self.client.get('/平臺項目列表/揣列表', {
            '關鍵字': '水母'
        })
# 		前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['列表'], [])

    def test_無文本當做揣無(self):
        self.資料庫加外語('水母')
#         前端輸入
        回應 = self.client.get('/平臺項目列表/揣列表', {
            '關鍵字': '水母'
        })
#         前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['列表'], [])

    def test_文本無建議用字當做揣無(self):
        水母編號 = self.資料庫加外語('水母')
        平臺項目表.外語翻母語(水母編號, {
            '文本資料': '媠',
        })
#         前端輸入
        回應 = self.client.get('/平臺項目列表/揣列表', {
            '關鍵字': '水母'
        })
#         前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['列表'], [])

    def test_文本有建議用字就揣會著(self):
        水母編號 = self.資料庫加外語('水母')
        文本 = 平臺項目表.外語翻母語(水母編號, {
            '文本資料': '䖳',
        })
        文本.設為推薦用字()
#         前端輸入
        回應 = self.client.get('/平臺項目列表/揣列表', {
            '關鍵字': '水母'
        })
#         前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['列表'][0]['新詞文本'][0]['文本資料'], '䖳')

    def test_有頓票資料(self):
        水母編號 = self.資料庫加外語('水母')
        文本 = 平臺項目表.外語翻母語(水母編號, {
            '文本資料': '䖳',
        })
        文本.設為推薦用字()
#         前端輸入
        回應 = self.client.get('/平臺項目列表/揣列表', {
            '關鍵字': '水母'
        })
#         前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertIn('按呢講好', 回應資料['列表'][0]['新詞文本'][0])

    def test_對應華語(self):
        水母編號 = self.資料庫加外語('水母')
        文本 = 平臺項目表.外語翻母語(水母編號, {
            '文本資料': '䖳',
        })
        文本.設為推薦用字()
#         前端輸入
        回應 = self.client.get('/平臺項目列表/揣列表', {
            '關鍵字': '水母'
        })
#         前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertIn('水母', str(回應資料['列表'][0]['新詞文本'][0]['按呢講的外語列表']))

    def test_文本有閣校對過就揣會著(self):
        漂亮編號 = self.資料庫加外語('漂亮')
        文本 = 平臺項目表.外語翻母語(漂亮編號, {
            '文本資料': '3',
        })
        新文本 = 平臺項目表._校對母語文本(文本.編號(), {
            '文本資料': '媠',
            '屬性': {'音標': 'sui2'}
        })
        新文本.設為推薦用字()
#         前端輸入
        回應 = self.client.get('/平臺項目列表/揣列表', {
            '關鍵字': '漂亮'
        })
#         前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['列表'][0]['新詞文本'][0]['文本資料'], '媠')

    def test_文本有兩組建議用字(self):
        水母編號 = self.資料庫加外語('水母')
        文本 = 平臺項目表.外語翻母語(水母編號, {
            '文本資料': '䖳',
        })
        文本.設為推薦用字()
        文本 = 平臺項目表.外語翻母語(水母編號, {
            '文本資料': '水母',
        })
        文本.設為推薦用字()
#         前端輸入
        回應 = self.client.get('/平臺項目列表/揣列表', {
            '關鍵字': '水母'
        })
#         前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(len(回應資料['列表']), 1)

    def test_相像袂使出現(self):
        水母編號 = self.資料庫加外語('水母')
        水母腦編號 = self.資料庫加外語('水母腦')
        水母國編號 = self.資料庫加外語('水母國')
        握手編號 = self.資料庫加外語('握手')
        for 編號 in [水母編號, 水母腦編號, 水母國編號, 握手編號]:
            self.外語有建議的文本(編號)
# 		前端輸入
        回應 = self.client.get('/平臺項目列表/揣列表', {
            '關鍵字': '水母'
        })
# 		前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(len(回應資料['列表']), 1)

    def test_貢獻者愛是頭一个文本的來源(self):
        漂亮編號 = self.資料庫加外語('漂亮')
        文本 = 平臺項目表.外語翻母語(漂亮編號, {
            '來源': {'名': 'pigu'},
            '文本資料': '3',
        })
        新文本 = 平臺項目表._校對母語文本(文本.編號(), {
            '來源': {'名': 'bauzak'},
            '文本資料': '媠',
            '屬性': {'音標': 'sui2'}
        })
        新文本.設為推薦用字()
#         前端輸入
        回應 = self.client.get('/平臺項目列表/揣列表', {
            '關鍵字': '漂亮'
        })
#         前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['列表'][0]['新詞文本'][0]['貢獻者'], 'pigu')

    def test_人講好就排頭前(self):
        水母編號 = self.資料庫加外語('水母')
        䖳文本 = 平臺項目表.外語翻母語(水母編號, {
            '文本資料': '䖳',
        })
        䖳文本.按呢講好 += 1
        䖳文本.設為推薦用字()
        水母文本 = 平臺項目表.外語翻母語(水母編號, {
            '文本資料': '水母',
        })
        水母文本.按呢無好 += 1
        水母文本.設為推薦用字()
        一九文本 = 平臺項目表.外語翻母語(水母編號, {
            '文本資料': '一九',
        })
        一九文本.按呢講好 += 1
        一九文本.按呢無好 += 1
        一九文本.設為推薦用字()
#         前端輸入
        回應 = self.client.get('/平臺項目列表/揣列表', {
            '關鍵字': '水母'
        })
#         前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['列表'][0]['新詞文本'][0]['文本資料'], '䖳')
        self.assertEqual(回應資料['列表'][0]['新詞文本'][1]['文本資料'], '一九')
        self.assertEqual(回應資料['列表'][0]['新詞文本'][2]['文本資料'], '水母')

    def test_無傳關鍵字(self):
        # 		前端輸入
        回應 = self.client.get('/平臺項目列表/揣列表', {
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

    def 外語有建議的文本(self, 外語編號):
        文本 = 平臺項目表.外語翻母語(外語編號, {
            '文本資料': 'the7',
        })
        文本.推薦用字 = True
        文本.save()
