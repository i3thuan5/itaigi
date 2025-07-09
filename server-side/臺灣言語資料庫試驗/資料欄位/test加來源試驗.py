# -*- coding: utf-8 -*-
from django.test import TestCase
import json
from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語資料庫.資料模型 import 來源屬性表


class 加來源試驗(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_來源內容(self):
        Pigu = 來源表.加來源({'名': 'Dr. Pigu', '出世年': '1990', '出世地': '花蓮', })
        self.assertEqual(Pigu.名, 'Dr. Pigu')

    def test_來源數量(self):
        來源表.加來源({'名': 'Dr. Pigu', '出世年': '1990', '出世地': '花蓮', })
        self.assertEqual(來源表.objects.all().count(), 1)

    def test_屬性內容欄位(self):
        Pigu = 來源表.加來源({'名': 'Dr. Pigu', '出世年': '1990', '出世地': '花蓮', })
        self.assertEqual(Pigu.屬性.count(), 2)
        self.assertEqual(Pigu.屬性.get(分類='出世年').分類, '出世年')
        self.assertEqual(json.loads(Pigu.屬性.get(分類='出世年').性質), '1990')
        self.assertEqual(Pigu.屬性.get(分類='出世年').內容(), {'出世年': '1990'})
        self.assertEqual(Pigu.屬性.get(分類='出世地').分類, '出世地')
        self.assertEqual(json.loads(Pigu.屬性.get(分類='出世地').性質), '花蓮')
        self.assertEqual(Pigu.屬性.get(分類='出世地').內容(), {'出世地': '花蓮'})

    def test_屬性內容函式(self):
        Pigu = 來源表.加來源({'名': 'Dr. Pigu', '出世年': '1990', '出世地': '花蓮', })
        self.assertEqual(Pigu.屬性內容(), {'出世年': '1990', '出世地': '花蓮', })

    def test_屬性數量(self):
        來源表.加來源({'名': 'Dr. Pigu', '出世年': '1990', '出世地': '花蓮', })
        self.assertEqual(來源屬性表.objects.all().count(), 2)

    def test_無屬性來源內容(self):
        Pigu = 來源表.加來源({'名': 'Dr. Pigu', })
        self.assertEqual(Pigu.名, 'Dr. Pigu')

    def test_無屬性來源數量(self):
        來源表.加來源({'名': 'Dr. Pigu', })
        self.assertEqual(來源表.objects.all().count(), 1)

    def test_無屬性屬性內容欄位(self):
        Pigu = 來源表.加來源({'名': 'Dr. Pigu', })
        self.assertEqual(Pigu.屬性.count(), 0)

    def test_無屬性屬性內容函式(self):
        Pigu = 來源表.加來源({'名': 'Dr. Pigu', })
        self.assertEqual(Pigu.屬性內容(), {})

    def test_無屬性屬性數量(self):
        來源表.加來源({'名': 'Dr. Pigu', })
        self.assertEqual(來源屬性表.objects.all().count(), 0)

    def test_仝屬性共用來源內容(self):
        來源表.加來源({'名': 'Dr. Pigu', '出世年': '1990', '出世地': '花蓮', })
        Mrs = 來源表.加來源({'名': 'Mrs. Pigu', '出世年': '1990', '出世地': '吉安', })
        self.assertEqual(Mrs.名, 'Mrs. Pigu')

    def test_仝屬性共用來源數量(self):
        來源表.加來源({'名': 'Dr. Pigu', '出世年': '1990', '出世地': '花蓮', })
        self.assertEqual(來源表.objects.all().count(), 1)
        來源表.加來源({'名': 'Mrs. Pigu', '出世年': '1990', '出世地': '吉安', })
        self.assertEqual(來源表.objects.all().count(), 2)

    def test_仝屬性共用屬性內容欄位(self):
        來源表.加來源({'名': 'Dr. Pigu', '出世年': '1990', '出世地': '花蓮', })
        Mrs = 來源表.加來源({'名': 'Mrs. Pigu', '出世年': '1990', '出世地': '吉安', })
        self.assertEqual(Mrs.屬性.count(), 2)
        self.assertEqual(Mrs.屬性.get(分類='出世年').分類, '出世年')
        self.assertEqual(json.loads(Mrs.屬性.get(分類='出世年').性質), '1990')
        self.assertEqual(Mrs.屬性.get(分類='出世年').內容(), {'出世年': '1990'})
        self.assertEqual(Mrs.屬性.get(分類='出世地').分類, '出世地')
        self.assertEqual(json.loads(Mrs.屬性.get(分類='出世地').性質), '吉安')
        self.assertEqual(Mrs.屬性.get(分類='出世地').內容(), {'出世地': '吉安'})

    def test_仝屬性共用屬性內容函式(self):
        來源表.加來源({'名': 'Dr. Pigu', '出世年': '1990', '出世地': '花蓮', })
        Mrs = 來源表.加來源({'名': 'Mrs. Pigu', '出世年': '1990', '出世地': '吉安', })
        self.assertEqual(Mrs.屬性內容(), {'出世年': '1990', '出世地': '吉安', })

    def test_仝屬性共用屬性數量(self):
        來源表.加來源({'名': 'Dr. Pigu', '出世年': '1990', '出世地': '花蓮', })
        self.assertEqual(來源屬性表.objects.all().count(), 2)
        來源表.加來源({'名': 'Mrs. Pigu', '出世年': '1990', '出世地': '吉安', })
        self.assertEqual(來源屬性表.objects.all().count(), 3)

    def test_仝名無仝屬性來源內容(self):
        少年Pigu = 來源表.加來源({'名': 'Dr. Pigu', '出世年': '1990', })
        self.assertEqual(少年Pigu.名, 'Dr. Pigu')
        完整Pigu = 來源表.加來源({'名': 'Dr. Pigu', '出世年': '1990', '出世地': '花蓮', })
        self.assertEqual(完整Pigu.名, 'Dr. Pigu')
        無屬性Pigu = 來源表.加來源({'名': 'Dr. Pigu', })
        self.assertEqual(無屬性Pigu.名, 'Dr. Pigu')
        職業Pigu = 來源表.加來源({'名': 'Dr. Pigu', '職業': '學生', })
        self.assertEqual(職業Pigu.名, 'Dr. Pigu')

    def test_仝名無仝屬性來源數量(self):
        來源表.加來源({'名': 'Dr. Pigu', '出世年': '1990', })
        self.assertEqual(來源表.objects.all().count(), 1)
        來源表.加來源({'名': 'Dr. Pigu', '出世年': '1990', '出世地': '花蓮', })
        self.assertEqual(來源表.objects.all().count(), 2)
        來源表.加來源({'名': 'Dr. Pigu', })
        self.assertEqual(來源表.objects.all().count(), 3)
        來源表.加來源({'名': 'Dr. Pigu', '職業': '學生', })
        self.assertEqual(來源表.objects.all().count(), 4)

    def test_仝名無仝屬性屬性內容欄位(self):
        少年Pigu = 來源表.加來源({'名': 'Dr. Pigu', '出世年': '1990', })
        self.assertEqual(少年Pigu.屬性.count(), 1)
        self.assertEqual(少年Pigu.屬性.get(分類='出世年').分類, '出世年')
        self.assertEqual(json.loads(少年Pigu.屬性.get(分類='出世年').性質), '1990')
        self.assertEqual(少年Pigu.屬性.get(分類='出世年').內容(), {'出世年': '1990'})
        完整Pigu = 來源表.加來源({'名': 'Dr. Pigu', '出世年': '1990', '出世地': '花蓮', })
        self.assertEqual(完整Pigu.屬性.count(), 2)
        self.assertEqual(完整Pigu.屬性.get(分類='出世年').分類, '出世年')
        self.assertEqual(json.loads(完整Pigu.屬性.get(分類='出世年').性質), '1990')
        self.assertEqual(完整Pigu.屬性.get(分類='出世年').內容(), {'出世年': '1990'})
        self.assertEqual(完整Pigu.屬性.get(分類='出世地').分類, '出世地')
        self.assertEqual(json.loads(完整Pigu.屬性.get(分類='出世地').性質), '花蓮')
        self.assertEqual(完整Pigu.屬性.get(分類='出世地').內容(), {'出世地': '花蓮'})
        無屬性Pigu = 來源表.加來源({'名': 'Dr. Pigu', })
        self.assertEqual(無屬性Pigu.屬性.count(), 0)
        職業Pigu = 來源表.加來源({'名': 'Dr. Pigu', '職業': '學生', })
        self.assertEqual(職業Pigu.屬性.count(), 1)
        self.assertEqual(職業Pigu.屬性.get(分類='職業').分類, '職業')
        self.assertEqual(json.loads(職業Pigu.屬性.get(分類='職業').性質), '學生')
        self.assertEqual(職業Pigu.屬性.get(分類='職業').內容(), {'職業': '學生'})

    def test_仝名無仝屬性屬性內容函式(self):
        少年Pigu = 來源表.加來源({'名': 'Dr. Pigu', '出世年': '1990', })
        self.assertEqual(少年Pigu.屬性內容(), {'出世年': '1990', })
        完整Pigu = 來源表.加來源({'名': 'Dr. Pigu', '出世年': '1990', '出世地': '花蓮', })
        self.assertEqual(完整Pigu.屬性內容(), {'出世年': '1990', '出世地': '花蓮', })
        無屬性Pigu = 來源表.加來源({'名': 'Dr. Pigu', })
        self.assertEqual(無屬性Pigu.屬性內容(), {})
        職業Pigu = 來源表.加來源({'名': 'Dr. Pigu', '職業': '學生', })
        self.assertEqual(職業Pigu.屬性內容(), {'職業': '學生', })

    def test_仝名無仝屬性屬性數量(self):
        來源表.加來源({'名': 'Dr. Pigu', '出世年': '1990', })
        self.assertEqual(來源屬性表.objects.all().count(), 1)
        來源表.加來源({'名': 'Dr. Pigu', '出世年': '1990', '出世地': '花蓮', })
        self.assertEqual(來源屬性表.objects.all().count(), 2)
        來源表.加來源({'名': 'Dr. Pigu', })
        self.assertEqual(來源屬性表.objects.all().count(), 2)
        來源表.加來源({'名': 'Dr. Pigu', '職業': '學生', })
        self.assertEqual(來源屬性表.objects.all().count(), 3)

    def test_無名的錯誤(self):
        self.assertRaises(
            KeyError, 來源表.加來源, {'姓名': 'Dr. Pigu', '出世年': '1990', })
