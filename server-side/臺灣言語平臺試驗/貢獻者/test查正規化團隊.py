# -*- coding: utf-8 -*-
from 臺灣言語平臺.項目模型 import 平臺項目表


from django.urls.base import resolve
from django.test import TestCase


from 臺灣言語平臺.介面.貢獻者 import 正規化團隊表


class 查貢獻者表試驗(TestCase):

    def test_有對應函式(self):
        對應 = resolve('/正規化團隊表')
        self.assertEqual(對應.func, 正規化團隊表)

    def test_新正規化(self):
        漂亮編號 = self.資料庫加外語('漂亮')
        文本 = 平臺項目表.外語翻母語(漂亮編號, {
            '文本資料': '3',
        })
        平臺項目表.對正規化sheet校對母語文本(
            文本.編號(), 'pigu', '媠', 'sui2',
        )

        回應Json = self.client.get('/正規化團隊表').json()
        self.assertEqual(len(回應Json['名人']), 1)
        self.assertEqual(回應Json['名人'][0]['數量'], 1)
        self.assertEqual(回應Json['名人'][0]['名'], 'pigu')

    def test_照數量排(self):
        漂亮1編號 = self.資料庫加外語('漂亮1')
        文本1 = 平臺項目表.外語翻母語(漂亮1編號, {'文本資料': '3', })
        平臺項目表.對正規化sheet校對母語文本(
            文本1.編號(), 'ciciw', '媠', 'sui2',
        )
        漂亮2編號 = self.資料庫加外語('漂亮2')
        文本2 = 平臺項目表.外語翻母語(漂亮2編號, {'文本資料': '3', })
        平臺項目表.對正規化sheet校對母語文本(
            文本2.編號(), 'fafoy', '媠', 'sui2',
        )

        漂亮3編號 = self.資料庫加外語('漂亮3')
        文本3 = 平臺項目表.外語翻母語(漂亮3編號, {'文本資料': '3', })
        平臺項目表.對正規化sheet校對母語文本(
            文本3.編號(), 'fafoy', '媠', 'sui2',
        )

        回應Json = self.client.get('/正規化團隊表').json()
        self.assertEqual(回應Json, {
            '名人': [
                {'名': 'fafoy', '數量': 2},
                {'名': 'ciciw', '數量': 1},
            ]
        })

    def 資料庫加外語(self, 外語詞):
        return 平臺項目表.加外語資料(
            {
                '外語資料': 外語詞,
            }
        ).編號()
