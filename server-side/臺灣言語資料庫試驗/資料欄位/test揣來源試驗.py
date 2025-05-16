# -*- coding: utf-8 -*-
from django.test import TestCase
from 臺灣言語資料庫.資料模型 import 來源表
from django.core.exceptions import ObjectDoesNotExist
from 臺灣言語資料庫.資料模型 import 來源屬性表


class 揣來源試驗(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_一般來源(self):
        Pigu = 來源表.加來源({'名': 'Dr. Pigu', '出世年': '1990', '出世地': '花蓮', })
        揣著 = 來源表.揣來源({'名': 'Dr. Pigu', '出世年': '1990', '出世地': '花蓮', })
        self.assertEqual(揣著, Pigu)

    def test_無屬性來源(self):
        Pigu = 來源表.加來源({'名': 'Dr. Pigu', })
        揣著 = 來源表.揣來源({'名': 'Dr. Pigu', })
        self.assertEqual(揣著, Pigu)

    def test_仝屬性共用(self):
        Dr = 來源表.加來源({'名': 'Dr. Pigu', '出世年': '1990', '出世地': '花蓮', })
        Mrs = 來源表.加來源({'名': 'Mrs. Pigu', '出世年': '1990', '出世地': '吉安', })
        self.assertEqual(
            來源表.揣來源({'名': 'Dr. Pigu', '出世年': '1990', '出世地': '花蓮', }), Dr)
        self.assertEqual(
            來源表.揣來源({'名': 'Mrs. Pigu', '出世年': '1990', '出世地': '吉安', }), Mrs)

    def test_仝名無仝屬性(self):
        少年Pigu = 來源表.加來源({'名': 'Dr. Pigu', '出世年': '1990', })
        完整Pigu = 來源表.加來源({'名': 'Dr. Pigu', '出世年': '1990', '出世地': '花蓮', })
        無屬性Pigu = 來源表.加來源({'名': 'Dr. Pigu', })
        職業Pigu = 來源表.加來源({'名': 'Dr. Pigu', '職業': '學生', })
        揣著 = 來源表.揣來源({'名': 'Dr. Pigu', '職業': '學生', })
        self.assertEqual(揣著, 職業Pigu)
        揣著 = 來源表.揣來源({'名': 'Dr. Pigu', })
        self.assertEqual(揣著, 無屬性Pigu)
        揣著 = 來源表.揣來源({'名': 'Dr. Pigu', '出世年': '1990', })
        self.assertEqual(揣著, 少年Pigu)
        揣著 = 來源表.揣來源({'名': 'Dr. Pigu', '出世年': '1990', '出世地': '花蓮', })
        self.assertEqual(揣著, 完整Pigu)

    def test_仝屬性揣無(self):
        來源表.加來源({'名': 'Dr. Pigu', '出世年': '1990', '出世地': '花蓮', })
        with self.assertRaises(ObjectDoesNotExist):
            來源表.揣來源(
                {'名': 'Mrs. Pigu', '出世年': '1990', '出世地': '吉安', }
            )

    def test_仝名無仝屬性揣無(self):
        來源表.加來源({'名': 'Dr. Pigu', '出世年': '1990', '出世地': '花蓮', })
        來源表.加來源({'名': 'Dr. Pigu', })
        來源表.加來源({'名': 'Dr. Pigu', '職業': '學生', })
        self.assertRaises(ObjectDoesNotExist,
                          來源表.揣來源, {'名': 'Dr. Pigu', '出世年': '1990', })

    def test_無仝屬性嘛是袂使(self):
        來源表.加來源({'名': 'Dr. Pigu', '出世年': '1990', '出世地': '花蓮', })
        來源表.加來源({'名': 'Dr. Pigu', '出世年': '1990', })
        來源表.加來源({'名': 'Dr. Pigu', '職業': '學生', })
        self.assertRaises(ObjectDoesNotExist,
                          來源表.揣來源, {'名': 'Dr. Pigu', })

    def test_揣無來源袂使加來源資料(self):
        來源表.加來源({'名': 'Dr. Pigu', '出世年': '1990', '出世地': '花蓮', })
        來源數量 = 來源表.objects.all().count()

        with self.assertRaises(ObjectDoesNotExist):
            來源表.揣來源(
                {'名': 'Dr. Pigu', '出世年': '1990', '職業': '學生', }
            )
        self.assertEqual(來源表.objects.all().count(), 來源數量)

    def test_揣無來源袂使加屬性(self):
        來源表.加來源({'名': 'Dr. Pigu', '出世年': '1990', '出世地': '花蓮', })
        來源屬性數量 = 來源屬性表.objects.all().count()

        with self.assertRaises(ObjectDoesNotExist):
            來源表.揣來源(
                {'名': 'Dr. Pigu', '出世年': '1990', '職業': '學生', }
            )
        self.assertEqual(來源屬性表.objects.all().count(), 來源屬性數量)
