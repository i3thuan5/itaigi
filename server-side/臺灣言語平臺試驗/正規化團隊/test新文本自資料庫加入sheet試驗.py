import json
from unittest.mock import patch
from os.path import abspath, dirname, join

from django.test.testcases import TestCase


from 臺灣言語平臺.項目模型 import 平臺項目表
from 臺灣言語資料庫.資料模型 import 語言腔口表
from 臺灣言語平臺.正規化團隊模型 import 正規化sheet表
from 臺灣言語平臺.使用者模型 import 使用者表


class 新文本自資料庫加入sheet試驗(TestCase):

    json檔名 = join(dirname(abspath(__file__)), '資料', 'itaigi-ae98ec2616c9.json')

    def setUp(self):
        self.阿媠 = 使用者表.加使用者('sui2@pigu.tw', {'名': '阿媠'})
        self.client.force_login(self.阿媠)

        臺灣語言 = 語言腔口表.objects.create(語言腔口='臺灣語言')
        正規化sheet表.objects.create(
            key_file_name=self.json檔名,
            url='http://ti1tiau5.tw',
            語言腔口=臺灣語言
        )

    def _加公家內容(self, 資料內容):
        return 資料內容

    @patch('臺灣言語平臺.tasks.新文本自資料庫加入sheet.delay')
    def test_加外語新詞有叫函式(self, 文本加入sheetMocka):
        self.client.force_login(self.阿媠)
        外語回應 = self.client.post(
            '/平臺項目/加外語', self._加公家內容({
                '屬性': json.dumps({'詞性': '形容詞', '字數': '2'}),
                '外語語言': '華語',
                '外語資料': '漂亮',
            })
        )
        外語回應資料 = 外語回應.json()
        外語項目編號 = int(外語回應資料['平臺項目編號'])
        回應 = self.client.post(
            '/平臺項目/加新詞文本', self._加公家內容({
                '外語項目編號': 外語項目編號,
                '屬性': json.dumps({'詞性': '形容詞', '字數': '1'}),
                '文本資料': '媠',
            })
        )
        回應資料 = json.loads(回應.content.decode("utf-8"))
        文本加入sheetMocka.assert_called_once_with(回應資料['平臺項目編號'])

    @patch('臺灣言語平臺.正規化團隊模型.正規化sheet表._編號有佇表內底無')
    @patch('gspread.authorize')
    def test_有看全部的資料(self, authorizeMocka, 有佇表內底無mocka):
        文本項目 = self.加入新文本()
        正規化sheet表.文本加入sheet(文本項目.編號())
        self.assertEqual(有佇表內底無mocka.call_count, 1)

    @patch('gspread.authorize')
    def test_有檢查重覆資料(self, authorizeMocka):
        資料表mocka = authorizeMocka.return_value.open_by_url.return_value.sheet1
        文本項目 = self.加入新文本()
        正規化sheet表.文本加入sheet(文本項目.編號())
        資料表mocka.col_values.assert_called_once_with(1)

    @patch('gspread.authorize')
    def test_重覆資料袂加第二擺(self, authorizeMocka):
        資料表mocka = authorizeMocka.return_value.open_by_url.return_value.sheet1
        文本項目 = self.加入新文本()
        資料表mocka.col_values.return_value = [
            '流水號',
            str(文本項目.編號()),
        ]
        正規化sheet表.文本加入sheet(文本項目.編號())
        資料表mocka.append_row.assert_not_called()

    @patch('gspread.authorize')
    def test_有加資料進去(self, authorizeMocka):
        資料表mocka = authorizeMocka.return_value.open_by_url.return_value.sheet1
        文本項目 = self.加入新文本()
        正規化sheet表.文本加入sheet(文本項目.編號())
        資料表mocka.append_row.assert_called_once_with(
            [str(文本項目.編號()), '阿媠', '漂亮', '媠', '', '', '', '', '', '']
        )

    @patch('gspread.authorize')
    def test_加有音標的資料進去(self, authorizeMocka):
        資料表mocka = authorizeMocka.return_value.open_by_url.return_value.sheet1
        外語項目 = 平臺項目表.加外語資料(self._加公家內容({
            '屬性': json.dumps({'詞性': '形容詞', '字數': '2'}),
            '外語語言': '華語',
            '外語資料': '漂亮',
        }))
        文本項目 = 平臺項目表.外語翻母語(
            外語項目.編號(),
            self._加公家內容({
                '收錄者': self.阿媠.來源,
                '屬性': json.dumps({'音標': 'sui2', '字數': '1'}),
                '文本資料': '媠',
            })
        )
        正規化sheet表.文本加入sheet(文本項目.編號())
        資料表mocka.append_row.assert_called_once_with(
            [str(文本項目.編號()), '阿媠', '漂亮', '媠', 'sui2', '', '', '', '', '']
        )

    @patch('gspread.authorize')
    def test_有校對資料就莫閣加入去(self, authorizeMocka):
        資料表mocka = authorizeMocka.return_value.open_by_url.return_value.sheet1
        文本項目 = self.加入新文本()
        新資料 = self._加公家內容({
            '屬性': json.dumps({'詞性': '形容詞', '字數': '1'}),
            '文本資料': '媠媠',
        })
        平臺項目表._校對母語文本(文本項目.編號(), 新資料)
        正規化sheet表.文本加入sheet(文本項目.編號())
        資料表mocka.append_row.assert_not_called()

    @patch('gspread.authorize')
    def test_無sheet資料就莫校做代誌(self, authorizeMocka):
        正規化sheet表.objects.all().delete()
        資料表mocka = authorizeMocka.return_value.open_by_url.return_value.sheet1
        文本項目 = self.加入新文本()
        正規化sheet表.文本加入sheet(文本項目.編號())
        資料表mocka.append_row.assert_not_called()

    def 加入新文本(self):
        外語項目 = 平臺項目表.加外語資料(self._加公家內容({
            '屬性': json.dumps({'詞性': '形容詞', '字數': '2'}),
            '外語語言': '華語',
            '外語資料': '漂亮',
        }))
        文本項目 = 平臺項目表.外語翻母語(
            外語項目.編號(),
            self._加公家內容({
                '收錄者': self.阿媠.來源,
                '屬性': json.dumps({'詞性': '形容詞', '字數': '1'}),
                '文本資料': '媠',
            })
        )
        return 文本項目
