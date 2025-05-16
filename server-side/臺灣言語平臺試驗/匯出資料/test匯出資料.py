# -*- coding: utf-8 -*-
from 臺灣言語平臺.項目模型 import 平臺項目表


import json

from django.urls.base import resolve
from django.test import TestCase


from 臺灣言語平臺.使用者模型 import 使用者表
from 臺灣言語平臺.介面.匯出資料 import 匯出辭典資料


class 匯出資料試驗(TestCase):

    def setUp(self):
        self.貢獻者 = 使用者表.加使用者(
            'contributor@itaigi.tw',
            {'名': '貢獻者1號', '出世年': '1987', '出世地': '臺灣', }
        )
        self.貢獻者.set_password('Phoo-bun')
        self.貢獻者.save()

        外語回應 = self.client.post(
            '/平臺項目/加外語', {
                '外語資料': '漂亮'
            }
        )

        外語回應資料 = json.loads(外語回應.content.decode("utf-8"))
        self.外語項目編號 = int(外語回應資料['平臺項目編號'])

        self.外語 = 平臺項目表.objects.get(pk=self.外語項目編號).外語

    def test_有對應函式(self):
        對應 = resolve('/匯出資料')
        self.assertEqual(對應.func, 匯出辭典資料)

    def test_新增貢獻確認結果(self):
        self.client.force_login(self.貢獻者)

        回應 = self.client.post(
            '/平臺項目/加新詞文本', {
                '外語項目編號': self.外語項目編號,
                '文本資料': '水',
                '音標資料': 'suie',
            }
        )

        平臺項目編號 = 回應.json()['平臺項目編號']
        平臺項目 = 平臺項目表.揣編號(平臺項目編號)
        平臺項目.對正規化sheet校對母語文本(
            平臺項目編號, '正規化團隊一號團員', '媠', 'sui2'
        )

        回應 = self.client.get('/匯出資料')
        回應Json = 回應.json()
        self.assertEqual(len(回應Json['資料']), 1)
        self.assertEqual(回應Json['資料'][0]['華語'], '漂亮')
        self.assertEqual(回應Json['資料'][0]['來源'], '貢獻者1號')
        self.assertEqual(回應Json['資料'][0]['漢字'], '媠')
        self.assertEqual(回應Json['資料'][0]['羅馬字'], 'sui2')

    def test_新增著的貢獻(self):
        self.client.force_login(self.貢獻者)

        回應 = self.client.post(
            '/平臺項目/加新詞文本', {
                '外語項目編號': self.外語項目編號,
                '文本資料': '媠',
                '音標資料': 'sui2',
            }
        )

        平臺項目編號 = 回應.json()['平臺項目編號']
        平臺項目表.揣編號(平臺項目編號).設為推薦用字()

        回應 = self.client.get('/匯出資料')
        回應Json = 回應.json()
        self.assertEqual(len(回應Json['資料']), 1)
        self.assertEqual(回應Json['資料'][0]['華語'], '漂亮')
        self.assertEqual(回應Json['資料'][0]['來源'], '貢獻者1號')
        self.assertEqual(回應Json['資料'][0]['漢字'], '媠')
        self.assertEqual(回應Json['資料'][0]['羅馬字'], 'sui2')
