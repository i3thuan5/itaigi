# -*- coding: utf-8 -*-
import json

from django.urls.base import resolve
from django.test import TestCase


from 臺灣言語平臺.項目模型 import 平臺項目表
from 臺灣言語平臺.介面.加資料 import 加外語請教條
from 臺灣言語平臺.介面.改資料 import 把測試資料藏起來
from 臺灣言語平臺.使用者模型 import 使用者表


class 外語藏起來試驗(TestCase):

    def setUp(self):
        self.鄉民 = 使用者表.加使用者(
            'sui2@pigu.tw', {"名": '鄉民', '出世年': '1950', '出世地': '臺灣', }
        )
        self.鄉民.set_password('Phoo-bun')
        self.鄉民.save()

    def test_有對應函式(self):
        對應 = resolve('/平臺項目/加外語')
        self.assertEqual(對應.func, 加外語請教條)
        對應 = resolve('/平臺項目/把測試資料藏起來')
        self.assertEqual(對應.func, 把測試資料藏起來)

    def test_有功能(self):
        self.client.force_login(self.鄉民)
        回應 = self.client.post(
            '/平臺項目/加外語', {
                '外語資料': '果汁123',  # 不設限，隨意增加
            }
        )
        self.assertEqual(回應.status_code, 200)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertEqual(回應資料, {
            '平臺項目編號': 回應資料['平臺項目編號'],
        })
#       後端資料庫檢查
        編號 = int(回應資料['平臺項目編號'])

        外語 = 平臺項目表.objects.get(pk=編號)
        self.assertEqual(外語.愛藏起來, False)
        回應 = self.client.post(
            '/平臺項目/把測試資料藏起來', {
                '資料編號': 編號,
            }
        )
        外語 = 平臺項目表.objects.get(pk=編號)
        self.assertEqual(外語.愛藏起來, True)

    def test_失敗的json回應(self):
        self.client.force_login(self.鄉民)
        回應 = self.client.post(
            '/平臺項目/把測試資料藏起來', {
                '資料編號': 'abcd',
            }
        )
        self.assertEqual(json.loads(回應.content.decode("utf-8")), {
            "錯誤": "資料編號只能是數字",
        })
