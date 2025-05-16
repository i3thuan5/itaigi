from django.test.testcases import TestCase
from 臺灣言語資料庫.資料模型 import 文本表
from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語資料庫.資料模型 import 版權表
from 臺灣言語資料庫.欄位資訊 import 會使公開
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音


class 文本分詞資料(TestCase):

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
        }

    def test_文本爾(self):
        self.詞內容['文本資料'] = '豬仔'
        文本 = 文本表.加資料(self.詞內容)
        self.assertEqual(文本.分詞資料(), '豬-仔')

    def test_文本佮音標(self):
        self.詞內容['文本資料'] = '豬仔'
        self.詞內容['音標資料'] = 'ti1-a2'
        文本 = 文本表.加資料(self.詞內容)
        self.assertEqual(文本.分詞資料(), '豬-仔｜ti1-a2')

    def test_減號一堆(self):
        self.詞內容['文本資料'] = '------------呵-------------'
        文本 = 文本表.加資料(self.詞內容)
        self.assertEqual(
            文本.分詞資料(),
            '- - - - - - - - - - - - 呵 - - - - - - - - - - - - -'
        )

    def test_減號一堆嘛袂使影響拼音(self):
        self.詞內容['文本資料'] = '---呵 li2-ho2'
        文本 = 文本表.加資料(self.詞內容)
        self.assertEqual(文本.分詞資料(臺灣閩南語羅馬字拼音), '- - - 呵 li2-ho2')

    def test_分詞符號換做一般pipe符號(self):
        self.詞內容['文本資料'] = '｜＝安姑＝｜＝＝表小弟'
        文本 = 文本表.加資料(self.詞內容)
        self.assertEqual(文本.分詞資料(), '| ＝ 安-姑 ＝ | ＝ ＝ 表-小-弟')

    def test_文本顯示(self):
        self.詞內容['文本資料'] = '------------呵-------------'
        文本 = 文本表.加資料(self.詞內容)
        self.assertEqual(str(文本), '------------呵-------------')
