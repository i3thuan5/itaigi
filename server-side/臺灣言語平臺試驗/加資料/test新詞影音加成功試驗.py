# -*- coding: utf-8 -*-
from 臺灣言語資料庫.資料模型 import 外語表
from 臺灣言語資料庫.資料模型 import 影音表
import io
import json
import wave

from django.urls.base import resolve
from django.test import TestCase


from 臺灣言語資料庫.關係模型 import 翻譯影音表
from 臺灣言語平臺.項目模型 import 平臺項目表
from 臺灣言語平臺.介面.加資料 import 加新詞影音
from 臺灣言語平臺.使用者模型 import 使用者表


class 新詞影音加成功試驗(TestCase):

    def setUp(self):
        super(新詞影音加成功試驗, self).setUp()
        self.鄉民 = 使用者表.加使用者(
            'sui2@pigu.tw', {"名": '鄉民', '出世年': '1950', '出世地': '臺灣', }
        )
        self.鄉民.set_password('Phoo-bun')
        self.鄉民.save()

        外語回應 = self.client.post(
            '/平臺項目/加外語', {
                '外語資料': '漂亮',
            }
        )
        外語回應資料 = json.loads(外語回應.content.decode("utf-8"))
        self.外語項目編號 = int(外語回應資料['平臺項目編號'])
        self.外語 = 平臺項目表.objects.get(pk=self.外語項目編號).外語

        self.檔案 = io.BytesIO()
        with wave.open(self.檔案, 'wb') as 音檔:
            音檔.setnchannels(1)
            音檔.setframerate(16000)
            音檔.setsampwidth(2)
            音檔.writeframesraw(b'sui2' * 20)
        self.檔案.seek(0)
        self.檔案.name = '試驗音檔'

        self.外語表資料數 = 外語表.objects.all().count()
        self.影音表資料數 = 影音表.objects.all().count()
        self.翻譯影音表資料數 = 翻譯影音表.objects.all().count()
        self.平臺項目表資料數 = 平臺項目表.objects.all().count()

    def test_有對應函式(self):
        對應 = resolve('/平臺項目/加新詞影音')
        self.assertEqual(對應.func, 加新詞影音)

    def test_來源自己(self):
        self.client.force_login(self.鄉民)
        回應 = self.client.post(
            '/平臺項目/加新詞影音', {
                '外語項目編號': self.外語項目編號,
                '來源': json.dumps('自己'),  # 可用「自己」，會把來源指向自己
                '影音資料': self.檔案,
            }
        )
        self.assertEqual(回應.status_code, 200)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertIn('平臺項目編號', 回應資料)
# 		後端資料庫檢查
        self.assertEqual(外語表.objects.all().count(), self.外語表資料數)
        self.assertEqual(影音表.objects.all().count(), self.影音表資料數 + 1)
        self.assertEqual(翻譯影音表.objects.all().count(), self.翻譯影音表資料數 + 1)
        編號 = int(回應資料['平臺項目編號'])

        影音 = 平臺項目表.objects.get(pk=編號).影音
        self.外語.翻譯影音.get(影音=影音)
        self.assertEqual(影音.收錄者.使用者, self.鄉民)
        self.assertEqual(影音.來源.使用者, self.鄉民)

    def test_來源名自己(self):
        self.client.force_login(self.鄉民)
        回應 = self.client.post(
            '/平臺項目/加新詞影音', {
                '外語項目編號': self.外語項目編號,
                '來源': json.dumps({'名': '自己'}),  # 當作一个人叫做「自己」
                '影音資料': self.檔案,
            }
        )
        self.assertEqual(回應.status_code, 200)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertIn('平臺項目編號', 回應資料)
# 		後端資料庫檢查
        self.assertEqual(外語表.objects.all().count(), self.外語表資料數)
        self.assertEqual(影音表.objects.all().count(), self.影音表資料數 + 1)
        self.assertEqual(翻譯影音表.objects.all().count(), self.翻譯影音表資料數 + 1)
        編號 = int(回應資料['平臺項目編號'])

        影音 = 平臺項目表.objects.get(pk=編號).影音
        self.外語.翻譯影音.get(影音=影音)
        self.assertEqual(影音.收錄者.使用者, self.鄉民)
        self.assertEqual(影音.來源.名, '自己')
        self.assertEqual(影音.來源.屬性.count(), 0)

    def test_無登入(self):
        self.client.logout()
        回應 = self.client.post(
            '/平臺項目/加新詞影音', {
                '外語項目編號': self.外語項目編號,
                '影音資料': self.檔案,
            }
        )
        self.assertEqual(回應.status_code, 200)
#         後端資料庫檢查
        回應資料 = 回應.json()
        self.assertEqual(外語表.objects.all().count(), self.外語表資料數)
        self.assertEqual(影音表.objects.all().count(), self.影音表資料數 + 1)
        self.assertEqual(翻譯影音表.objects.all().count(), self.翻譯影音表資料數 + 1)
        self.assertEqual(平臺項目表.objects.all().count(), self.平臺項目表資料數 + 1)
        編號 = int(回應資料['平臺項目編號'])

        影音 = 平臺項目表.objects.get(pk=編號).影音
        self.外語.翻譯影音.get(影音=影音)
        self.assertEqual(影音.收錄者.名, '匿名')
        self.assertEqual(影音.來源.名, '匿名')

    def test_仝款資料加兩擺(self):
        '影音比較的成本太大，所以不檢查'
        self.client.post(
            '/平臺項目/加新詞影音', {
                '外語項目編號': self.外語項目編號,
                '影音資料': self.檔案,
            }
        )
        self.檔案.seek(0)
        回應 = self.client.post(
            '/平臺項目/加新詞影音', {
                '外語項目編號': self.外語項目編號,
                '影音資料': self.檔案,
            }
        )
        self.assertEqual(回應.status_code, 200)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertIn('平臺項目編號', 回應資料)
#         後端資料庫檢查
        self.assertEqual(外語表.objects.all().count(), self.外語表資料數)
        self.assertEqual(影音表.objects.all().count(), self.影音表資料數 + 2)
        self.assertEqual(翻譯影音表.objects.all().count(), self.翻譯影音表資料數 + 2)
        self.assertEqual(平臺項目表.objects.all().count(), self.平臺項目表資料數 + 2)
        編號 = int(回應資料['平臺項目編號'])

        影音 = 平臺項目表.objects.get(pk=編號).影音
        self.外語.翻譯影音.get(影音=影音)  # 確定有建立關係
        self.assertEqual(影音.影音資料.read(), self.檔案.getvalue())

    def test_預設參數(self):
        回應 = self.client.post(
            '/平臺項目/加新詞影音', {  # 全部都必須字串形態
                '外語項目編號': self.外語項目編號,  # 針對哪一個外語的母語影音
                '影音資料': self.檔案,  # 錄製的影音檔，檔案型態
            }
        )
        self.assertEqual(回應.status_code, 200)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertIn('平臺項目編號', 回應資料)
#         後端資料庫檢查
        self.assertEqual(外語表.objects.all().count(), self.外語表資料數)
        self.assertEqual(影音表.objects.all().count(), self.影音表資料數 + 1)
        self.assertEqual(翻譯影音表.objects.all().count(), self.翻譯影音表資料數 + 1)
        self.assertEqual(平臺項目表.objects.all().count(), self.平臺項目表資料數 + 1)
        編號 = int(回應資料['平臺項目編號'])

        影音 = 平臺項目表.objects.get(pk=編號).影音
        self.外語.翻譯影音.get(影音=影音)  # 確定有建立關係
        self.assertEqual(影音.收錄者.名, '匿名')
        self.assertEqual(影音.來源.名, '匿名')
        self.assertEqual(影音.版權.版權, '會使公開')
        self.assertEqual(影音.種類.種類, '字詞')
        self.assertEqual(影音.語言腔口.語言腔口, '臺灣語言')
        self.assertEqual(影音.著作所在地.著作所在地, '臺灣')
        self.assertGreaterEqual(影音.著作年.著作年, '2016')
        self.assertEqual(影音.屬性.count(), 0)
