import io
import wave

from django.test.testcases import TestCase


from 臺灣言語資料庫.資料模型 import 影音表
from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語資料庫.資料模型 import 版權表
from os.path import isfile


class 影音所在試驗(TestCase):

    def setUp(self):
        self.句檔案 = io.BytesIO()
        with wave.open(self.句檔案, 'wb') as 音檔:
            音檔.setnchannels(1)
            音檔.setframerate(16000)
            音檔.setsampwidth(2)
            音檔.writeframesraw(b'sui2' * 80000)
        self.詞內容 = {
            '收錄者': 來源表.objects.get_or_create(名='系統管理員')[0],
            '來源': {'名': 'Konn', },
            '版權': 版權表.objects.get_or_create(版權='會使公開')[0],
            '種類': '語句',
            '語言腔口': '閩南語',
            '著作所在地': '花蓮',
            '著作年': '2016',
            '影音資料': self.句檔案,
        }

    def tearDown(self):
        self.句檔案.close()

    def test_愛絕對路徑(self):
        資料 = 影音表.加資料(self.詞內容)
        self.assertTrue(資料.影音所在().startswith('/'))
        self.assertTrue(isfile(資料.影音所在()))

    def test_無設media_root(self):
        with self.settings(MEDIA_ROOT=''):
            資料 = 影音表.加資料(self.詞內容)
            self.assertTrue(資料.影音所在().startswith('/'))
            self.assertTrue(isfile(資料.影音所在()))
