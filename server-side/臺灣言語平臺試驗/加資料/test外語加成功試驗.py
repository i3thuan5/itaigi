# -*- coding: utf-8 -*-
import json

from django.urls.base import resolve
from django.test import TestCase


from 臺灣言語資料庫.資料模型 import 外語表
from 臺灣言語平臺.項目模型 import 平臺項目表
from 臺灣言語平臺.介面.加資料 import 加外語請教條
from 臺灣言語平臺.使用者模型 import 使用者表


class 外語加成功試驗(TestCase):

    def setUp(self):
        self.鄉民 = 使用者表.加使用者(
            'sui2@pigu.tw', {"名": '鄉民', '出世年': '1950', '出世地': '臺灣', }
        )
        self.鄉民.set_password('Phoo-bun')
        self.鄉民.save()

    def test_有對應函式(self):
        對應 = resolve('/平臺項目/加外語')
        self.assertEqual(對應.func, 加外語請教條)

    def test_無登入(self):
        回應 = self.client.post(
            '/平臺項目/加外語', {
                '外語資料': '漂亮',
            }
        )
        self.assertEqual(回應.status_code, 200)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertEqual(回應資料, {
            '平臺項目編號': 回應資料['平臺項目編號'],
        })
#         後端資料庫檢查
        編號 = int(回應資料['平臺項目編號'])

        外語 = 平臺項目表.objects.get(pk=編號).外語
        self.assertEqual(外語.收錄者.名, '匿名')
        self.assertEqual(外語.收錄者.屬性.count(), 0)
        self.assertEqual(外語.來源.名, '匿名')
        self.assertEqual(外語.來源.屬性.count(), 0)

    def test_有登入(self):
        self.client.force_login(self.鄉民)
        回應 = self.client.post(
            '/平臺項目/加外語', {
                '外語資料': '漂亮',  # 不設限，隨意增加
            }
        )
        self.assertEqual(回應.status_code, 200)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertEqual(回應資料, {
            '平臺項目編號': 回應資料['平臺項目編號'],
        })
# 		後端資料庫檢查
        編號 = int(回應資料['平臺項目編號'])

        外語 = 平臺項目表.objects.get(pk=編號).外語
        self.assertEqual(外語.收錄者.使用者, self.鄉民)

    def test_有來源(self):
        回應 = self.client.post(
            '/平臺項目/加外語', {
                '外語資料': '漂亮',
                '來源': json.dumps({'名': '阿媠', '職業': '學生'}),
            }
        )
        self.assertEqual(回應.status_code, 200)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertEqual(回應資料, {
            '平臺項目編號': 回應資料['平臺項目編號'],
        })
        編號 = int(回應資料['平臺項目編號'])

        外語 = 平臺項目表.objects.get(pk=編號).外語
        self.assertEqual(外語.來源.名, '阿媠')
        self.assertEqual(外語.來源.屬性.count(), 1)
        self.assertEqual(外語.來源.屬性.get().內容(), {'職業': '學生'})

    def test_預設欄位(self):
        回應 = self.client.post(
            '/平臺項目/加外語', {
                '外語資料': '漂亮',  # 不設限，隨意增加
            }
        )
        self.assertEqual(回應.status_code, 200)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertEqual(回應資料, {
            '平臺項目編號': 回應資料['平臺項目編號'],
        })
#         後端資料庫檢查
        編號 = int(回應資料['平臺項目編號'])

        外語 = 平臺項目表.objects.get(pk=編號).外語
        self.assertEqual(外語.版權.版權, '會使公開')
        self.assertEqual(外語.種類.種類, '字詞')
        self.assertEqual(外語.語言腔口.語言腔口, '臺灣語言')
        self.assertEqual(外語.著作所在地.著作所在地, '臺灣')
        self.assertGreaterEqual(int(外語.著作年.著作年), 2015)
        self.assertEqual(外語.外語語言.語言腔口, '華語')
        self.assertEqual(外語.外語資料, '漂亮')

    def test_來源預設是自己(self):
        self.client.force_login(self.鄉民)
        回應 = self.client.post(
            '/平臺項目/加外語', {
                '來源': json.dumps('自己'),  # 可用「自己」，會把來源指向自己。一樣先轉成字串。
                '外語資料': '漂亮',
            }
        )
        self.assertEqual(回應.status_code, 200)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertEqual(回應資料, {
            '平臺項目編號': 回應資料['平臺項目編號'],
        })
# 		後端資料庫檢查
        編號 = int(回應資料['平臺項目編號'])

        外語 = 平臺項目表.objects.get(pk=編號).外語
        self.assertEqual(外語.收錄者.使用者, self.鄉民)
        self.assertEqual(外語.來源.使用者, self.鄉民)

    def test_來源名自己(self):
        self.client.force_login(self.鄉民)
        回應 = self.client.post(
            '/平臺項目/加外語', {
                '來源': json.dumps({'名': '自己'}),  # 當作一个人叫做「自己」
                '外語資料': '漂亮',
            }
        )
        self.assertEqual(回應.status_code, 200)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertEqual(回應資料, {
            '平臺項目編號': 回應資料['平臺項目編號'],
        })
# 		後端資料庫檢查
        編號 = int(回應資料['平臺項目編號'])

        外語 = 平臺項目表.objects.get(pk=編號).外語
        self.assertEqual(外語.收錄者.使用者, self.鄉民)
        self.assertEqual(外語.來源.名, '自己')
        self.assertEqual(外語.來源.屬性.count(), 0)

    def test_資料頭前後壁的空白愛提掉(self):
        回應 = self.client.post(
            '/平臺項目/加外語', {
                '外語資料': ' 漂亮 ',
            }
        )
        self.assertEqual(回應.status_code, 200)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertEqual(回應資料, {
            '平臺項目編號': 回應資料['平臺項目編號'],
        })
#         後端資料庫檢查
        編號 = int(回應資料['平臺項目編號'])

        外語 = 平臺項目表.objects.get(pk=編號).外語
        self.assertEqual(外語.外語資料, '漂亮')

    def test_仝款資料加兩擺(self):
        # 種類、語言腔口、外語語言、外語資料，四个攏仝款就袂使閣加矣
        self.client.force_login(self.鄉民)
        第一擺回應 = self.client.post(
            '/平臺項目/加外語', {
                '外語資料': '漂亮',
            }
        )
        第一擺回應資料 = json.loads(第一擺回應.content.decode("utf-8"))
        外語表資料數 = 外語表.objects.all().count()
        回應 = self.client.post(
            '/平臺項目/加外語', {
                '外語資料': '漂亮',
            }
        )
        self.assertEqual(回應.status_code, 200)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertEqual(回應資料, {
            '其他': '這個外語已經有了',
            '平臺項目編號': 第一擺回應資料['平臺項目編號'],
        })
        self.assertEqual(外語表資料數, 外語表.objects.all().count())
