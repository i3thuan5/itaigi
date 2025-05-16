import io
from re import search
from unittest.mock import patch

from django.core.management import call_command
from django.test.testcases import TestCase


from 臺灣言語資料庫.資料模型 import 資料表工具


class 顯示資料數量指令試驗(TestCase):

    @patch('臺灣言語資料庫.資料模型.資料表工具.顯示資料數量')
    def test_有叫顯示的函式(self, 顯示資料數量mocka):
        顯示資料數量mocka.side_effect = [
            '外語有2筆，影音有5筆，文本有33筆，聽拍有9筆'
        ]
        with io.StringIO() as out:
            call_command('顯示資料數量', stdout=out)
            self.assertIn('外語有2筆，影音有5筆，文本有33筆，聽拍有9筆', out.getvalue())

    def test_顯示資料狀態有資料數量(self):
        self.assertIsNotNone(
            search(
                r'外語有\d+筆，影音有\d+筆，文本有\d+筆，聽拍有\d+筆',
                資料表工具.顯示資料數量()
            )
        )
