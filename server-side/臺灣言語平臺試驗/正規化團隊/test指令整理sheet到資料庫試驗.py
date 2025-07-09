import io
import json
from unittest.mock import patch
from os.path import abspath, dirname, join

from django.core.management import call_command
from django.test.testcases import TestCase


from 臺灣言語平臺.正規化團隊模型 import 正規化sheet表
from 臺灣言語平臺.項目模型 import 平臺項目表
from 臺灣言語資料庫.資料模型 import 來源表


class 指令整理sheet到資料庫試驗(TestCase):

    json檔名 = join(dirname(abspath(__file__)), '資料', 'itaigi-ae98ec2616c9.json')

    @patch('臺灣言語平臺.正規化團隊模型.正規化sheet表.全部整理到資料庫')
    def test_有叫著全部整理函式(self, 全部整理到資料庫mocka):
        with io.StringIO() as 輸出:
            call_command(
                '整理全部sheet到資料庫', stdout=輸出
            )
        全部整理到資料庫mocka.assert_called_once_with()

    @patch('臺灣言語平臺.正規化團隊模型.正規化sheet表.全部資料')
    def test_有全部整理(self, 全部資料mocka):
        正規化sheet表.全部整理到資料庫()
        全部資料mocka.assert_called_once_with()

    @patch('臺灣言語平臺.正規化團隊模型.正規化sheet表.整理到資料庫')
    def test_有整理(self, 整理到資料庫mocka):
        self._加臺語sheet表()
        正規化sheet表.全部整理到資料庫()
        整理到資料庫mocka.assert_called_once_with()

    @patch('gspread.authorize')
    def test_有掠全部資料(self, authorizeMocka):
        臺語sheet表 = self._加臺語sheet表()
        臺語sheet表.整理到資料庫()
        資料表mocka = authorizeMocka.return_value.open_by_url.return_value.sheet1
        資料表mocka.get_all_values.assert_called_once_with()

    def test_有編輯新的愛設推薦用字(self):
        文本項目 = self._加入新文本()
        平臺項目表.對正規化sheet校對母語文本(文本項目.編號(), '編輯者', '媠媠', '')

        新文本 = 文本項目.校對後的文本()
        self.assertTrue(新文本.是推薦用字())

    def test_有編輯舊的愛取消推薦用字(self):
        文本項目 = self._加入新文本()
        文本項目.設為推薦用字()
        平臺項目表.對正規化sheet校對母語文本(文本項目.編號(), '編輯者', '媠媠', '')
        self.assertFalse(平臺項目表.揣編號(文本項目.編號()).是推薦用字())

    def _加臺語sheet表(self):
        return 正規化sheet表.加sheet(
            語言腔口='臺語',
            key_file_name=self.json檔名,
            url='https://itaigi.tw',
        )

    def _加入新文本(self):
        來源表.objects.get_or_create(名='阿媠')
        外語項目 = 平臺項目表.加外語資料({
            '收錄者': json.dumps({'名': '阿媠'}),
            '來源': json.dumps({'名': '阿媠'}),
            '外語資料': '漂亮',
        })
        文本項目 = 平臺項目表.外語翻母語(
            外語項目.編號(),
            {
                '收錄者': json.dumps({'名': '阿媠'}),
                '來源': json.dumps({'名': '阿媠'}),
                '文本資料': '媠',
            }
        )
        return 文本項目
