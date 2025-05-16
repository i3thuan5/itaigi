# -*- coding: utf-8 -*-
from 臺灣言語資料庫.資料模型 import 外語表
from 臺灣言語資料庫.資料模型 import 影音表
from 臺灣言語資料庫.資料模型 import 文本表
from 臺灣言語資料庫.關係模型 import 翻譯影音表
from 臺灣言語資料庫.關係模型 import 影音文本表
from 臺灣言語平臺.項目模型 import 平臺項目表


import json


from django.test import TestCase
from django.urls.base import resolve
from django.core.cache import cache

from 臺灣言語資料庫.關係模型 import 翻譯文本表
from 臺灣言語平臺.介面.貢獻者 import 貢獻者表
from 臺灣言語平臺.使用者模型 import 使用者表


class 查貢獻者表試驗(TestCase):

    def setUp(self):
        super(查貢獻者表試驗, self).setUp()
        # 多加一個使用者避免與測試與上線資料庫碰撞
        # 上線資料庫的臺灣閩南語常用詞辭典 id = 2
        # 但是由於 testing 會做新資料庫，所以貢獻者1號排第一位id會等於2
        # 故新增一個辭典來源避免這個問題
        self.辭典 = 使用者表.加使用者(
            'dictionary@itaigi.tw',
            {'名': '臺灣閩南語常用詞辭典', }
        )
        self.辭典.set_password('Kau-tian')
        self.辭典.save()
        self.貢獻者 = 使用者表.加使用者(
            'contributor@itaigi.tw',
            {'名': '貢獻者1號', '出世年': '1987', '出世地': '臺灣', }
        )
        self.貢獻者.set_password('Phoo-bun')
        self.貢獻者.save()
        """
        self.正規化團隊 = 使用者表.加使用者(
            'normal_form_team@itaigi.tw',
            {'名': '正規化團隊成員', '出世地': '臺灣', }
        )
        """

        self.有對應函式()

        外語回應 = self.client.post(
            '/平臺項目/加外語', {
                '外語資料': '漂亮'
            }
        )

        外語回應資料 = json.loads(外語回應.content.decode("utf-8"))
        self.外語項目編號 = int(外語回應資料['平臺項目編號'])

        self.外語 = 平臺項目表.objects.get(pk=self.外語項目編號).外語

        self.外語表資料數 = 外語表.objects.all().count()
        self.影音表資料數 = 影音表.objects.all().count()
        self.文本表資料數 = 文本表.objects.all().count()
        self.翻譯影音表資料數 = 翻譯影音表.objects.all().count()
        self.影音文本表資料數 = 影音文本表.objects.all().count()
        self.翻譯文本表資料數 = 翻譯文本表.objects.all().count()
        self.平臺項目表資料數 = 平臺項目表.objects.all().count()

    def tearDown(self):
        self.assertEqual(外語表.objects.all().count(), self.外語表資料數)
        self.assertEqual(影音表.objects.all().count(), self.影音表資料數)
        self.assertEqual(翻譯影音表.objects.all().count(), self.翻譯影音表資料數)
        self.assertEqual(影音文本表.objects.all().count(), self.影音文本表資料數)

    def 有對應函式(self):
        對應 = resolve('/貢獻者表')
        self.assertEqual(對應.func, 貢獻者表)

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

        回應 = self.client.get('/貢獻者表')
        回應Json = 回應.json()
        self.assertEqual(len(回應Json['名人']), 1)
        self.assertEqual(回應Json['名人'][0]['數量'], 1)
        self.assertEqual(回應Json['名人'][0]['名'], '貢獻者1號')

        self.assertEqual(文本表.objects.all().count(), self.文本表資料數 + 2)
        self.assertEqual(翻譯文本表.objects.all().count(), self.翻譯文本表資料數 + 1)
        self.assertEqual(平臺項目表.objects.all().count(), self.平臺項目表資料數 + 2)

    def test_新增著的貢獻(self):

        self.client.force_login(self.貢獻者)

        回應 = self.client.post(
            '/平臺項目/加新詞文本', {
                '外語項目編號': self.外語項目編號,
                '文本資料': '水',
                '音標資料': 'suie',
            }
        )

        平臺項目編號 = 回應.json()['平臺項目編號']
        平臺項目表.揣編號(平臺項目編號).設為推薦用字()

        回應 = self.client.get('/貢獻者表')
        回應Json = 回應.json()
        self.assertEqual(len(回應Json['名人']), 1)
        self.assertEqual(回應Json['名人'][0]['數量'], 1)
        self.assertEqual(回應Json['名人'][0]['名'], '貢獻者1號')

    def test_確認貢獻重覆詞條不同發音會被處理(self):

        貢獻文本資料 = ['水', '生著不醜']
        貢獻音標資料 = ['suie', 'se-liao-bei-bai']

        正規文本資料 = ['媠', '生做袂䆀']
        正規音標資料 = ['sui2', 'senn-tsò-bē-bái']

        self.client.force_login(self.貢獻者)

        self.assertEqual(len(貢獻文本資料), len(貢獻音標資料))
        self.assertEqual(len(正規文本資料), len(正規音標資料))

        for i in range(len(貢獻文本資料)):
            回應 = self.client.post(
                '/平臺項目/加新詞文本', {
                    '外語項目編號': self.外語項目編號,
                    '文本資料': 貢獻文本資料[i],
                    '音標資料': 貢獻音標資料[i],
                }
            )

            平臺項目編號 = 回應.json()['平臺項目編號']
            平臺項目 = 平臺項目表.揣編號(平臺項目編號)
            平臺項目.對正規化sheet校對母語文本(
                平臺項目編號, '正規化團隊一號團員',
                正規文本資料[i], 正規音標資料[i]
            )

        cache.clear()
        回應 = self.client.get('/貢獻者表')
        回應Json = 回應.json()
        self.assertEqual(len(回應Json['名人']), 1)
        self.assertEqual(回應Json['名人'][0]['數量'], 2)
        self.assertEqual(回應Json['名人'][0]['名'], '貢獻者1號')

        self.assertEqual(文本表.objects.all().count(), self.文本表資料數 + 4)
        self.assertEqual(翻譯文本表.objects.all().count(), self.翻譯文本表資料數 + 2)
        self.assertEqual(平臺項目表.objects.all().count(), self.平臺項目表資料數 + 4)

    def test_辭典的莫顯示(self):
        self.client.force_login(self.辭典)

        回應 = self.client.post(
            '/平臺項目/加新詞文本', {
                '外語項目編號': self.外語項目編號,
                '文本資料': '水',
                '音標資料': 'sui2',
            }
        )

        平臺項目編號 = 回應.json()['平臺項目編號']
        平臺項目表.揣編號(平臺項目編號).設為推薦用字()

        回應 = self.client.get('/貢獻者表')
        回應Json = 回應.json()
        self.assertEqual(len(回應Json['名人']), 0)
