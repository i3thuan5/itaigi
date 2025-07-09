import io
from os.path import join, dirname, abspath
from re import search
from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase


from 臺灣言語資料庫.匯出入 import 匯出入工具


class 匯入資料指令試驗(TestCase):

    @patch('臺灣言語資料庫.匯出入.匯出入工具._匯入物件')
    @patch('urllib.request.urlopen')
    def test_成功匯入網址(self, urlopenMocka, 匯入物件mocka):
        with io.StringIO() as out:
            call_command('匯入資料', 'http://意傳.台灣/臺灣言語資料庫.yaml', stdout=out)
            self.assertIn('「臺灣言語資料庫.yaml」匯入成功', out.getvalue())

    @patch('臺灣言語資料庫.匯出入.匯出入工具._匯入物件')
    def test_成功匯入檔案(self, 匯入物件mocka):
        with io.StringIO() as out:
            call_command(
                '匯入資料', join(dirname(abspath(__file__)), '資料', '全部相關資料組.yaml'), stdout=out)
            self.assertIn('「全部相關資料組.yaml」匯入成功', out.getvalue())

    @patch('臺灣言語資料庫.匯出入.匯出入工具._匯入物件')
    @patch('urllib.request.urlopen')
    def test_預設愛匯入影音(self, urlopenMocka, 匯入物件mocka):
        with io.StringIO() as out:
            call_command('匯入資料', 'http://意傳.台灣/臺灣言語資料庫.yaml', stdout=out)
        匯入物件mocka.assert_called_once_with(
            urlopenMocka.return_value.__enter__.return_value, None, True
        )

    @patch('臺灣言語資料庫.匯出入.匯出入工具._匯入物件')
    @patch('urllib.request.urlopen')
    def test_莫匯入影音(self, urlopenMocka, 匯入物件mocka):
        with io.StringIO() as out:
            call_command(
                '匯入資料',
                'http://意傳.台灣/臺灣言語資料庫.yaml',
                '--莫匯入影音',
                stdout=out
            )
        匯入物件mocka.assert_called_once_with(
            urlopenMocka.return_value.__enter__.return_value, None, False
        )

    def test_無網址(self):
        with self.assertRaises(CommandError):
            call_command('匯入資料')

    @patch('臺灣言語資料庫.匯出入.匯出入工具.顯示資料狀態')
    @patch('臺灣言語資料庫.匯出入.匯出入工具._匯入物件')
    @patch('urllib.request.urlopen')
    def test_愛算資料狀態(self, urlopenMocka, 匯入物件mocka, 顯示資料狀態mocka):
        顯示資料狀態mocka.return_value = 'Sui!'
        with io.StringIO() as out:
            call_command('匯入資料', 'http://意傳.台灣/臺灣言語資料庫.yaml', stdout=out)
        self.assertEqual(顯示資料狀態mocka.call_count, 2)

    @patch('臺灣言語資料庫.匯出入.匯出入工具.顯示資料狀態')
    @patch('臺灣言語資料庫.匯出入.匯出入工具._匯入物件')
    @patch('urllib.request.urlopen')
    def test_有顯示資料狀態(self, urlopenMocka, 匯入物件mocka, 顯示資料狀態mocka):
        顯示資料狀態mocka.side_effect = [
            '外語有0筆，影音有0筆，文本有0筆',
            '外語有2筆，影音有5筆，文本有33筆'
        ]
        with io.StringIO() as out:
            call_command('匯入資料', 'http://意傳.台灣/臺灣言語資料庫.yaml', stdout=out)
            self.assertIn('外語有0筆，影音有0筆，文本有0筆', out.getvalue())
            self.assertIn('外語有2筆，影音有5筆，文本有33筆', out.getvalue())

    @patch('臺灣言語資料庫.資料模型.資料表工具.顯示資料數量')
    def test_顯示資料狀態有資料數量(self, 顯示資料數量mocka):
        匯出入工具.顯示資料狀態()
        顯示資料數量mocka.assert_called_once_with()

    def test_顯示資料狀態有這馬時間(self):
        self.assertIsNotNone(
            search(
                r'這馬時間：\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}',
                匯出入工具.顯示資料狀態()
            )
        )

    @patch('臺灣言語資料庫.匯出入.匯出入工具._匯入物件')
    @patch('urllib.request.urlopen')
    def test_程式錯誤愛接起來(self, urlopenMocka, 匯入物件mocka):
        匯入物件mocka.side_effect = ValidationError('資料格式錯誤')
        with io.StringIO() as out:
            call_command('匯入資料', 'http://意傳.台灣/臺灣言語資料庫.yaml', stdout=out)
            self.assertIn('ValidationError', out.getvalue())
            self.assertIn('資料格式錯誤', out.getvalue())

    @patch('臺灣言語資料庫.匯出入.匯出入工具._匯入物件')
    @patch('urllib.request.urlopen')
    def test_程式錯誤匯入失敗愛顯示出來(self, urlopenMocka, 匯入物件mocka):
        匯入物件mocka.side_effect = ValidationError('資料格式錯誤')
        with io.StringIO() as out:
            call_command('匯入資料', 'http://意傳.台灣/臺灣言語資料庫.yaml', stdout=out)
            self.assertIn('「臺灣言語資料庫.yaml」匯入失敗', out.getvalue())

    @patch('臺灣言語資料庫.匯出入.匯出入工具.顯示資料狀態')
    @patch('臺灣言語資料庫.匯出入.匯出入工具._匯入物件')
    @patch('urllib.request.urlopen')
    def test_程式錯誤愛算資料狀態(self, urlopenMocka, 匯入物件mocka, 顯示資料狀態mocka):
        匯入物件mocka.side_effect = ValidationError('資料格式錯誤')
        顯示資料狀態mocka.return_value = 'Sui!'
        with io.StringIO() as out:
            call_command('匯入資料', 'http://意傳.台灣/臺灣言語資料庫.yaml', stdout=out)
        self.assertEqual(顯示資料狀態mocka.call_count, 2)
