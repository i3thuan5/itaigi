# -*- coding: utf-8 -*-
from django.urls.base import resolve
from django.test import TestCase


from 臺灣言語平臺.項目模型 import 平臺項目表
from 臺灣言語平臺.介面.看資料內容 import 投票


class 投票試驗(TestCase):

    def test_有對應函式(self):
        對應 = resolve('/平臺項目/投票')
        self.assertEqual(對應.func, 投票)

    def test_按呢講好(self):
        外語項目 = 平臺項目表.加外語資料({'外語資料': '水母'})
        文本項目 = 平臺項目表.外語翻母語(外語項目.編號(), {'文本資料': 'the7'})
        回應 = self.client.post(
            '/平臺項目/投票', {'平臺項目編號': 文本項目.編號(), 'decision': '按呢講好'}
        )

        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertIn('suId', 回應資料)
        self.assertIn('success', 回應資料)

    def test_按呢無好(self):
        外語項目 = 平臺項目表.加外語資料({'外語資料': '水母'})
        文本項目 = 平臺項目表.外語翻母語(外語項目.編號(), {'文本資料': 'the7'})
        回應 = self.client.post(
            '/平臺項目/投票', {'平臺項目編號': 文本項目.編號(), 'decision': '按呢無好'}
        )

        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertIn('suId', 回應資料)
        self.assertIn('success', 回應資料)

    def test_烏白傳講了按怎(self):
        外語項目 = 平臺項目表.加外語資料({'外語資料': '水母'})
        文本項目 = 平臺項目表.外語翻母語(外語項目.編號(), {'文本資料': 'the7'})
        回應 = self.client.post(
            '/平臺項目/投票', {'平臺項目編號': 文本項目.編號(), 'decision': '按呢……'}
        )

        self.assertEqual(回應.status_code, 400)
