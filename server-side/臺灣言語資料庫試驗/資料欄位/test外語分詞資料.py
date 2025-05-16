from django.test.testcases import TestCase
from 臺灣言語資料庫.資料模型 import 外語表
from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語資料庫.資料模型 import 版權表
from 臺灣言語資料庫.欄位資訊 import 會使公開


class 外語分詞資料(TestCase):

    def setUp(self):
        self.Pigu = 來源表.objects.create(名='Dr. Pigu')
        self.會使公開 = 版權表.objects.create(版權=會使公開)
        self.詞內容 = {
            '收錄者': {'名': 'Dr. Pigu'},
            '來源': {'名': 'Dr. Pigu'},
            '版權': '會使公開',
            '種類': '字詞',
            '語言腔口': '閩南語',
            '著作所在地': '花蓮',
            '著作年': '2016',
            '外語語言': '華語',
        }

    def test_外語爾(self):
        self.詞內容['外語資料'] = '小豬'
        外語 = 外語表.加資料(self.詞內容)
        self.assertEqual(外語.分詞資料(), '小-豬')

    def test_減號一堆(self):
        self.詞內容['外語資料'] = '------------呵-------------'
        外語 = 外語表.加資料(self.詞內容)
        self.assertEqual(
            外語.分詞資料(),
            '- - - - - - - - - - - - 呵 - - - - - - - - - - - - -'
        )

    def test_分詞符號換做一般pipe符號(self):
        self.詞內容['外語資料'] = '｜＝安姑＝｜＝＝表弟'
        外語 = 外語表.加資料(self.詞內容)
        self.assertEqual(外語.分詞資料(), '| ＝ 安-姑 ＝ | ＝ ＝ 表-弟')

    def test_外語顯示(self):
        self.詞內容['外語資料'] = '｜＝安姑＝｜＝＝表弟'
        外語 = 外語表.加資料(self.詞內容)
        self.assertEqual(str(外語), '｜＝安姑＝｜＝＝表弟')
