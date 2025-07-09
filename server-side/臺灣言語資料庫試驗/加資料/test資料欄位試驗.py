from django.db.utils import IntegrityError
from django.test.testcases import TestCase
from 臺灣言語資料庫.資料模型 import 來源屬性表
from 臺灣言語資料庫.資料模型 import 語言腔口表


class 資料欄位試驗(TestCase):

    def test_語言腔口表袂使有仝款的物件(self):
        語言腔口表.objects.create(語言腔口='臺語')
        with self.assertRaises(IntegrityError):
            語言腔口表.objects.create(語言腔口='臺語')

    def test_來源屬性表袂使有仝款的物件(self):
        來源屬性表.objects.create(分類='類', 性質='性')
        with self.assertRaises(IntegrityError):
            來源屬性表.objects.create(分類='類', 性質='性')
