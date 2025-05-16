from os.path import abspath, dirname, join
from unittest.mock import patch

from django.core.management import call_command
from django.test.testcases import TestCase


from 臺灣言語平臺.正規化團隊模型 import 正規化sheet表
from 臺灣言語資料庫.資料模型 import 語言腔口表
import io


class 指令加sheet的json試驗(TestCase):

    json檔名 = join(dirname(abspath(__file__)), '資料', 'itaigi-ae98ec2616c9.json')

    @patch('臺灣言語平臺.正規化團隊模型.正規化sheet表.加sheet')
    def test_有加資料入去(self, 加sheetMocka):
        with io.StringIO() as 輸出:
            call_command(
                '加sheet的json',  self.json檔名, 'https://itaigi.tw',
                stdout=輸出
            )
        加sheetMocka.assert_called_once_with(
            語言腔口='臺灣語言',
            key_file_name=self.json檔名,
            url='https://itaigi.tw',
        )

    @patch('臺灣言語平臺.正規化團隊模型.正規化sheet表.加sheet')
    def test_提示email愛加入編輯者(self, 加sheetMocka):
        with io.StringIO() as 輸出:
            call_command(
                '加sheet的json',  self.json檔名, 'https://itaigi.tw',
                stdout=輸出
            )
            self.assertIn('愛記得', 輸出.getvalue())
            self.assertIn(
                'itaigi@developer.gserviceaccount.com', 輸出.getvalue()
            )

    def test_檔案無存在(self):
        with self.assertRaises(FileNotFoundError):
            call_command(
                '加sheet的json', 'json檔名.json', 'https://itaigi.tw'
            )

    def test_加sheet入去資料正確(self):
        正規化sheet表.加sheet(
            語言腔口='臺語',
            key_file_name=self.json檔名,
            url='https://itaigi.tw',
        )
        臺語sheet = 正規化sheet表.objects.get()
        self.assertEqual(臺語sheet.語言腔口.語言腔口, '臺語')
        self.assertEqual(
            臺語sheet.key_file_name, self.json檔名)
        self.assertEqual(臺語sheet.url, 'https://itaigi.tw')

    def test_加sheet有加語言腔口(self):
        語言腔口數量 = 語言腔口表.objects.all().count()
        正規化sheet表.加sheet(
            語言腔口='臺語',
            key_file_name=self.json檔名,
            url='https://itaigi.tw',
        )
        self.assertEqual(語言腔口表.objects.all().count(), 語言腔口數量 + 1)

    def test_加sheet有揣語言腔口(self):
        語言腔口表.objects.create(語言腔口='臺語')
        語言腔口數量 = 語言腔口表.objects.all().count()
        正規化sheet表.加sheet(
            語言腔口='臺語',
            key_file_name=self.json檔名,
            url='https://itaigi.tw',
        )
        self.assertEqual(語言腔口表.objects.all().count(), 語言腔口數量)
