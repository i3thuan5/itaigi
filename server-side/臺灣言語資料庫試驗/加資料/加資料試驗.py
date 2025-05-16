# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist, ValidationError
import json
from 臺灣言語資料庫.資料模型 import 語言腔口表
from 臺灣言語資料庫.資料模型 import 著作所在地表
from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語資料庫.資料模型 import 來源屬性表
from 臺灣言語資料庫.資料模型 import 版權表
from 臺灣言語資料庫.欄位資訊 import 會使公開
from 臺灣言語資料庫.欄位資訊 import 袂使公開
from 臺灣言語資料庫.資料模型 import 種類表
from 臺灣言語資料庫.欄位資訊 import 字詞
from 臺灣言語資料庫.欄位資訊 import 語句
from 臺灣言語資料庫.資料模型 import 著作年表


class 加資料試驗:

    def 加初始資料佮設定變數(self):
        self._加初始資料()
        self.詞屬性 = {'詞性': '形容詞'}
        self.詞內容 = {
            '收錄者': {'名': '鄉民', '出世年': '1950', '出世地': '臺灣'},
            '來源': {'名': 'Dr. Pigu', '出世年': '1990', '出世地': '花蓮人'},
            '版權': '會使公開',
            '種類': '字詞',
            '語言腔口': '閩南語',
            '著作所在地': '花蓮',
            '著作年': '2014',
            '屬性': self.詞屬性,
        }
        self.句屬性 = {'性質': '例句'}
        self.句內容 = {
            '收錄者': {'名': 'Dr. Pigu', '出世年': '1990', '出世地': '花蓮人'},
            '來源': {'名': '鄉民', '出世年': '1950', '出世地': '臺灣'},
            '版權': '袂使公開',
            '種類': '語句',
            '語言腔口': '四縣話',
            '著作所在地': '臺灣',
            '著作年': '195x',
            '屬性': self.句屬性,
        }

    def _加初始資料(self):
        self.會使公開 = 版權表.objects.create(版權=會使公開)
        self.袂使公開 = 版權表.objects.create(版權=袂使公開)
        self.字詞 = 種類表.objects.get(種類=字詞)
        self.語句 = 種類表.objects.get(種類=語句)
        self.臺灣 = 著作所在地表.objects.create(著作所在地='臺灣')
        self.花蓮 = 著作所在地表.objects.create(著作所在地='花蓮')
        self.鄉民 = 來源表.objects.create(名='鄉民')
        出世年一九五空 = 來源屬性表.objects.create(分類='出世年', 性質=json.dumps('1950'))
        出世地臺灣 = 來源屬性表.objects.create(分類='出世地', 性質=json.dumps('臺灣'))
        self.鄉民.屬性.add(出世年一九五空, 出世地臺灣)
        self.Pigu = 來源表.objects.create(名='Dr. Pigu')
        self.Pigu.屬性.add(
            來源屬性表.objects.create(分類='出世年', 性質=json.dumps('1990')),
            來源屬性表.objects.create(分類='出世地', 性質=json.dumps('花蓮人')),
        )
        self.閩南語 = 語言腔口表.objects.create(語言腔口='閩南語')
        self.四縣話 = 語言腔口表.objects.create(語言腔口='四縣話')
        self.噶哈巫 = 語言腔口表.objects.create(語言腔口='噶哈巫')
        self.華語 = 語言腔口表.objects.create(語言腔口='華語')
        self.英語 = 語言腔口表.objects.create(語言腔口='英語')
        self.二空一四 = 著作年表.objects.create(著作年='2014')
        self.一九五空年代 = 著作年表.objects.create(著作年='195x')

    def test_加詞(self):
        原來資料數 = self.資料表.objects.all().count()
        self.資料 = self.資料表.加資料(self.詞內容)
        self.assertEqual(self.資料表.objects.all().count(), 原來資料數 + 1)
        self.assertEqual(self.資料.收錄者, self.鄉民)
        self.assertEqual(self.資料.來源, self.Pigu)
        self.assertEqual(self.資料.版權, self.會使公開)
        self.assertEqual(self.資料.種類, self.字詞)
        self.assertEqual(self.資料.語言腔口, self.閩南語)
        self.assertEqual(self.資料.著作所在地, self.花蓮)
        self.assertEqual(self.資料.著作年, self.二空一四)
        self.比較屬性(self.資料, self.詞屬性)

    def test_加句(self):
        原來資料數 = self.資料表.objects.all().count()
        self.資料 = self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 原來資料數 + 1)
        self.assertEqual(self.資料.收錄者, self.Pigu)
        self.assertEqual(self.資料.來源, self.鄉民)
        self.assertEqual(self.資料.版權, self.袂使公開)
        self.assertEqual(self.資料.種類, self.語句)
        self.assertEqual(self.資料.語言腔口, self.四縣話)
        self.assertEqual(self.資料.著作所在地, self.臺灣)
        self.assertEqual(self.資料.著作年, self.一九五空年代)
        self.比較屬性(self.資料, self.句屬性)

    def test_濟个正常語料(self):
        self.test_加詞()
        self.test_加句()
        self.test_加句()
        self.test_加詞()
        self.test_加詞()
        self.test_加句()
        self.test_加句()

    def test_收錄者舊字串(self):
        self.句內容['收錄者'] = json.dumps(self.句內容['收錄者'])
        原來資料數 = self.資料表.objects.all().count()
        資料 = self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 原來資料數 + 1)
        self.assertEqual(資料.收錄者, self.Pigu)
        self.assertEqual(資料.來源, self.鄉民)
        self.assertEqual(資料.版權, self.袂使公開)
        self.assertEqual(資料.種類, self.語句)
        self.assertEqual(資料.語言腔口, self.四縣話)
        self.assertEqual(資料.著作所在地, self.臺灣)
        self.assertEqual(資料.著作年, self.一九五空年代)
        self.比較屬性(資料, self.句屬性)

    def test_收錄者舊編號(self):
        self.句內容['收錄者'] = self.Pigu.pk
        原來資料數 = self.資料表.objects.all().count()
        資料 = self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 原來資料數 + 1)
        self.assertEqual(資料.收錄者, self.Pigu)
        self.assertEqual(資料.來源, self.鄉民)
        self.assertEqual(資料.版權, self.袂使公開)
        self.assertEqual(資料.種類, self.語句)
        self.assertEqual(資料.語言腔口, self.四縣話)
        self.assertEqual(資料.著作所在地, self.臺灣)
        self.assertEqual(資料.著作年, self.一九五空年代)
        self.比較屬性(資料, self.句屬性)

    def test_收錄者新物件(self):
        self.句內容['收錄者'] = {'名': '阿媠', '職業': '學生'}
        self.assertRaises(ObjectDoesNotExist, self.資料表.加資料, self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)

    def test_收錄者新字串(self):
        self.句內容['收錄者'] = json.dumps({'名': '阿媠', '職業': '學生'})
        self.assertRaises(ObjectDoesNotExist, self.資料表.加資料, self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)

    def test_收錄者新編號(self):
        self.句內容['收錄者'] = 1990
        self.assertRaises(ObjectDoesNotExist, self.資料表.加資料, self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)

    def test_收錄者無(self):
        self.句內容.pop('收錄者')
        self.assertRaises(KeyError, self.資料表.加資料, self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)

    def test_收錄者毋是字典字串佮編號(self):
        self.句內容['收錄者'] = 1990.0830
        with self.assertRaises(ValueError):
            self.資料表.加資料(self.句內容)
        self.句內容['收錄者'] = ['阿媠']
        with self.assertRaises(ValueError):
            self.資料表.加資料(self.句內容)
        self.句內容['收錄者'] = {'阿媠'}
        with self.assertRaises(ValueError):
            self.資料表.加資料(self.句內容)
        self.句內容['收錄者'] = None
        with self.assertRaises(ValidationError):
            self.資料表.加資料(self.句內容)

    def test_來源舊字串(self):
        self.句內容['來源'] = json.dumps(self.句內容['來源'])
        原來資料數 = self.資料表.objects.all().count()
        資料 = self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 原來資料數 + 1)
        self.assertEqual(資料.收錄者, self.Pigu)
        self.assertEqual(資料.來源, self.鄉民)
        self.assertEqual(資料.版權, self.袂使公開)
        self.assertEqual(資料.種類, self.語句)
        self.assertEqual(資料.語言腔口, self.四縣話)
        self.assertEqual(資料.著作所在地, self.臺灣)
        self.assertEqual(資料.著作年, self.一九五空年代)
        self.比較屬性(資料, self.句屬性)

    def test_來源舊編號(self):
        self.句內容['來源'] = self.鄉民.pk
        原來資料數 = self.資料表.objects.all().count()
        資料 = self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 原來資料數 + 1)
        self.assertEqual(資料.收錄者, self.Pigu)
        self.assertEqual(資料.來源, self.鄉民)
        self.assertEqual(資料.版權, self.袂使公開)
        self.assertEqual(資料.種類, self.語句)
        self.assertEqual(資料.語言腔口, self.四縣話)
        self.assertEqual(資料.著作所在地, self.臺灣)
        self.assertEqual(資料.著作年, self.一九五空年代)
        self.比較屬性(資料, self.句屬性)

    def test_來源新物件(self):
        self.句內容['來源'] = {'名': '阿媠', '職業': '學生'}
        原來資料數 = self.資料表.objects.all().count()
        資料 = self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 原來資料數 + 1)
        self.assertEqual(資料.收錄者, self.Pigu)
        self.assertEqual(資料.來源.名, '阿媠')
        self.assertEqual(資料.來源.屬性.count(), 1)
        self.assertEqual(資料.來源.屬性.first().分類, '職業')
        self.assertEqual(json.loads(資料.來源.屬性.first().性質), '學生')
        self.assertEqual(資料.來源.屬性.first().內容(), {'職業': '學生'})
        self.assertEqual(資料.版權, self.袂使公開)
        self.assertEqual(資料.種類, self.語句)
        self.assertEqual(資料.語言腔口, self.四縣話)
        self.assertEqual(資料.著作所在地, self.臺灣)
        self.assertEqual(資料.著作年, self.一九五空年代)
        self.比較屬性(資料, self.句屬性)

    def test_來源新字串(self):
        self.句內容['來源'] = json.dumps({'名': '阿媠', '職業': '暴民', '興趣': '日語'})
        原來資料數 = self.資料表.objects.all().count()
        資料 = self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 原來資料數 + 1)
        self.assertEqual(資料.收錄者, self.Pigu)
        self.assertEqual(資料.來源.名, '阿媠')
        self.assertEqual(資料.來源.屬性.count(), 2)
        self.assertEqual(資料.來源.屬性.filter(分類='職業').count(), 1)
        self.assertIsInstance(資料.來源.屬性.get(分類='職業'), 來源屬性表)
        self.assertEqual(json.loads(資料.來源.屬性.filter(分類='職業').first().性質), '暴民')
        self.assertEqual(資料.來源.屬性.filter(分類='職業').first().內容(), {'職業': '暴民'})
        self.assertEqual(資料.來源.屬性.get(分類='興趣').分類, '興趣')
        self.assertEqual(json.loads(資料.來源.屬性.get(分類='興趣').性質), '日語')
        self.assertEqual(資料.來源.屬性.get(分類='興趣').內容(), {'興趣': '日語'})
        self.assertEqual(資料.版權, self.袂使公開)
        self.assertEqual(資料.種類, self.語句)
        self.assertEqual(資料.語言腔口, self.四縣話)
        self.assertEqual(資料.著作所在地, self.臺灣)
        self.assertEqual(資料.著作年, self.一九五空年代)
        self.比較屬性(資料, self.句屬性)

    def test_來源物件有仝款欄位(self):
        self.句內容['來源'] = {'名': '阿媠', '職業': '暴民', '興趣': '日語'}
        原來資料數 = self.資料表.objects.all().count()
        資料 = self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 原來資料數 + 1)
        self.assertEqual(資料.收錄者, self.Pigu)
        self.assertEqual(資料.來源.名, '阿媠')
        self.assertEqual(資料.來源.屬性.count(), 2)
        self.assertEqual(資料.來源.屬性.filter(分類='職業').count(), 1)
        self.assertIsInstance(資料.來源.屬性.filter(分類='職業').get(), 來源屬性表)
        self.assertEqual(
            json.loads(資料.來源.屬性.filter(分類='職業').get().性質),  '暴民')
        self.assertEqual(資料.來源.屬性.get(分類='興趣').分類, '興趣')
        self.assertEqual(json.loads(資料.來源.屬性.get(分類='興趣').性質), '日語')
        self.assertEqual(資料.來源.屬性.get(分類='興趣').內容(), {'興趣': '日語'})
        self.assertEqual(資料.版權, self.袂使公開)
        self.assertEqual(資料.種類, self.語句)
        self.assertEqual(資料.語言腔口, self.四縣話)
        self.assertEqual(資料.著作所在地, self.臺灣)
        self.assertEqual(資料.著作年, self.一九五空年代)
        self.比較屬性(資料, self.句屬性)

    def test_來源新物件無名(self):
        self.句內容['來源'] = {'姓名': '阿媠', '職業': '學生'}
        self.assertRaises(KeyError, self.資料表.加資料, self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)

    def test_來源新字串無名(self):
        self.句內容['來源'] = json.dumps({'姓名': '阿媠', '職業': '學生'})
        self.assertRaises(KeyError, self.資料表.加資料, self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)

    def test_來源新編號(self):
        self.句內容['來源'] = 200
        self.assertRaises(ObjectDoesNotExist, self.資料表.加資料, self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)

    def test_來源無效字串(self):
        self.句內容['來源'] = '名'
        with self.assertRaises(ValueError):
            self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)

    def test_來源無(self):
        self.句內容.pop('來源')
        self.assertRaises(KeyError, self.資料表.加資料, self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)

    def test_來源毋是字典字串佮編號(self):
        self.句內容['來源'] = 1990.0328
        with self.assertRaises(ValueError):
            self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)
        self.句內容['來源'] = ['阿緣']
        with self.assertRaises(ValueError):
            self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)
        self.句內容['來源'] = {'阿緣'}
        with self.assertRaises(ValueError):
            self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)
        self.句內容['來源'] = None
        with self.assertRaises(ValidationError):
            self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)

    def test_版權舊編號(self):
        self.句內容['版權'] = self.袂使公開.pk
        原來資料數 = self.資料表.objects.all().count()
        資料 = self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 原來資料數 + 1)
        self.assertEqual(資料.收錄者, self.Pigu)
        self.assertEqual(資料.來源, self.鄉民)
        self.assertEqual(資料.版權, self.袂使公開)
        self.assertEqual(資料.種類, self.語句)
        self.assertEqual(資料.語言腔口, self.四縣話)
        self.assertEqual(資料.著作所在地, self.臺灣)
        self.assertEqual(資料.著作年, self.一九五空年代)
        self.比較屬性(資料, self.句屬性)

    def test_版權新字串(self):
        self.句內容['版權'] = '攏會使'
        self.assertRaises(ObjectDoesNotExist, self.資料表.加資料, self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)

    def test_版權新編號(self):
        self.句內容['版權'] = 2815
        self.assertRaises(ObjectDoesNotExist, self.資料表.加資料, self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)

    def test_版權無(self):
        self.句內容.pop('版權')
        self.assertRaises(KeyError, self.資料表.加資料, self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)

    def test_版權毋是字串佮編號(self):
        self.句內容['版權'] = 1990.0328
        with self.assertRaises(ValueError):
            self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)
        self.句內容['版權'] = ['阿投']
        with self.assertRaises(ValueError):
            self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)
        self.句內容['版權'] = None
        with self.assertRaises(ValidationError):
            self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)

    def test_種類舊編號(self):
        self.句內容['種類'] = self.語句.pk
        原來資料數 = self.資料表.objects.all().count()
        資料 = self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 原來資料數 + 1)
        self.assertEqual(資料.收錄者, self.Pigu)
        self.assertEqual(資料.來源, self.鄉民)
        self.assertEqual(資料.版權, self.袂使公開)
        self.assertEqual(資料.種類, self.語句)
        self.assertEqual(資料.語言腔口, self.四縣話)
        self.assertEqual(資料.著作所在地, self.臺灣)
        self.assertEqual(資料.著作年, self.一九五空年代)
        self.比較屬性(資料, self.句屬性)

    def test_種類新字串(self):
        self.句內容['種類'] = '課本'
        self.assertRaises(ObjectDoesNotExist, self.資料表.加資料, self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)

    def test_種類新編號(self):
        self.句內容['種類'] = -5
        self.assertRaises(ObjectDoesNotExist, self.資料表.加資料, self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)

    def test_種類無(self):
        self.句內容.pop('種類')
        self.assertRaises(KeyError, self.資料表.加資料, self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)

    def test_種類毋是字串佮編號(self):
        self.句內容['種類'] = 1115.12
        with self.assertRaises(ValueError):
            self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)
        self.句內容['種類'] = ['過年']
        with self.assertRaises(ValueError):
            self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)
        self.句內容['種類'] = None
        with self.assertRaises(ValidationError):
            self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)

    def test_語言腔口舊編號(self):
        self.句內容['語言腔口'] = self.四縣話.pk
        原來資料數 = self.資料表.objects.all().count()
        資料 = self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 原來資料數 + 1)
        self.assertEqual(資料.收錄者, self.Pigu)
        self.assertEqual(資料.來源, self.鄉民)
        self.assertEqual(資料.版權, self.袂使公開)
        self.assertEqual(資料.種類, self.語句)
        self.assertEqual(資料.語言腔口, self.四縣話)
        self.assertEqual(資料.著作所在地, self.臺灣)
        self.assertEqual(資料.著作年, self.一九五空年代)
        self.比較屬性(資料, self.句屬性)

    def test_語言腔口新字串(self):
        self.句內容['語言腔口'] = '豬豬語'
        原來資料數 = self.資料表.objects.all().count()
        資料 = self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 原來資料數 + 1)
        self.assertEqual(資料.收錄者, self.Pigu)
        self.assertEqual(資料.來源, self.鄉民)
        self.assertEqual(資料.版權, self.袂使公開)
        self.assertEqual(資料.種類, self.語句)
        self.assertEqual(資料.語言腔口.語言腔口, '豬豬語')
        self.assertEqual(資料.著作所在地, self.臺灣)
        self.assertEqual(資料.著作年, self.一九五空年代)
        self.比較屬性(資料, self.句屬性)

    def test_語言腔口新編號(self):
        self.句內容['語言腔口'] = 語言腔口表.objects.count() * 5
        self.assertRaises(ObjectDoesNotExist, self.資料表.加資料, self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)

    def test_語言腔口無(self):
        self.句內容.pop('語言腔口')
        self.assertRaises(KeyError, self.資料表.加資料, self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)

    def test_語言腔口毋是字串佮編號(self):
        self.句內容['語言腔口'] = 1115.12
        with self.assertRaises(ValueError):
            self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)
        self.句內容['語言腔口'] = ['噶哈巫', '四庄番']
        with self.assertRaises(ValueError):
            self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)
        self.句內容['語言腔口'] = None
        with self.assertRaises(ValidationError):
            self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)

    def test_著作所在地舊編號(self):
        self.句內容['著作所在地'] = self.臺灣.pk
        原來資料數 = self.資料表.objects.all().count()
        資料 = self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 原來資料數 + 1)
        self.assertEqual(資料.收錄者, self.Pigu)
        self.assertEqual(資料.來源, self.鄉民)
        self.assertEqual(資料.版權, self.袂使公開)
        self.assertEqual(資料.種類, self.語句)
        self.assertEqual(資料.語言腔口, self.四縣話)
        self.assertEqual(資料.著作所在地, self.臺灣)
        self.assertEqual(資料.著作年, self.一九五空年代)
        self.比較屬性(資料, self.句屬性)

    def test_著作所在地新字串(self):
        self.句內容['著作所在地'] = '埔里'
        原來資料數 = self.資料表.objects.all().count()
        資料 = self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 原來資料數 + 1)
        self.assertEqual(資料.收錄者, self.Pigu)
        self.assertEqual(資料.來源, self.鄉民)
        self.assertEqual(資料.版權, self.袂使公開)
        self.assertEqual(資料.種類, self.語句)
        self.assertEqual(資料.語言腔口, self.四縣話)
        self.assertEqual(資料.著作所在地.著作所在地, '埔里')
        self.assertEqual(資料.著作年, self.一九五空年代)
        self.比較屬性(資料, self.句屬性)

    def test_著作所在地新編號(self):
        self.句內容['著作所在地'] = 著作所在地表.objects.order_by('-pk').first().pk + 1
        self.assertRaises(ObjectDoesNotExist, self.資料表.加資料, self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)

    def test_著作所在地無(self):
        self.句內容.pop('著作所在地')
        self.assertRaises(KeyError, self.資料表.加資料, self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)

    def test_著作所在地毋是字串佮編號(self):
        self.句內容['著作所在地'] = 1115.12
        with self.assertRaises(ValueError):
            self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)
        self.句內容['著作所在地'] = {'守城份', '牛眠山', '大湳', '蜈蚣崙'}
        with self.assertRaises(ValueError):
            self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)
        self.句內容['著作所在地'] = None
        with self.assertRaises(ValidationError):
            self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)

    def test_著作年舊編號(self):
        self.句內容['著作年'] = self.一九五空年代.pk
        原來資料數 = self.資料表.objects.all().count()
        資料 = self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 原來資料數 + 1)
        self.assertEqual(資料.收錄者, self.Pigu)
        self.assertEqual(資料.來源, self.鄉民)
        self.assertEqual(資料.版權, self.袂使公開)
        self.assertEqual(資料.種類, self.語句)
        self.assertEqual(資料.語言腔口, self.四縣話)
        self.assertEqual(資料.著作所在地, self.臺灣)
        self.assertEqual(資料.著作年, self.一九五空年代)
        self.比較屬性(資料, self.句屬性)

    def test_著作年新字串(self):
        self.句內容['著作年'] = '19xx'
        原來資料數 = self.資料表.objects.all().count()
        資料 = self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 原來資料數 + 1)
        self.assertEqual(資料.收錄者, self.Pigu)
        self.assertEqual(資料.來源, self.鄉民)
        self.assertEqual(資料.版權, self.袂使公開)
        self.assertEqual(資料.種類, self.語句)
        self.assertEqual(資料.語言腔口, self.四縣話)
        self.assertEqual(資料.著作所在地, self.臺灣)
        self.assertEqual(資料.著作年.著作年, '19xx')
        self.比較屬性(資料, self.句屬性)

    def test_著作年新編號(self):
        self.句內容['著作年'] = 333
        self.assertRaises(ObjectDoesNotExist, self.資料表.加資料, self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)

    def test_著作年無(self):
        self.句內容.pop('著作年')
        self.assertRaises(KeyError, self.資料表.加資料, self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)

    def test_著作年毋是字串佮編號(self):
        self.句內容['著作年'] = 180.55

        with self.assertRaises(ValueError):
            self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)
        self.句內容['著作年'] = {'苗栗縣', '台中縣', '彰化縣'}
        with self.assertRaises(ValueError):
            self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)
        self.句內容['著作年'] = None
        with self.assertRaises(ValidationError):
            self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)

    def test_屬性是字串(self):
        self.句內容['屬性'] = json.dumps(self.句內容['屬性'])
        原來資料數 = self.資料表.objects.all().count()
        self.資料 = self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 原來資料數 + 1)
        self.assertEqual(self.資料.收錄者, self.Pigu)
        self.assertEqual(self.資料.來源, self.鄉民)
        self.assertEqual(self.資料.版權, self.袂使公開)
        self.assertEqual(self.資料.種類, self.語句)
        self.assertEqual(self.資料.語言腔口, self.四縣話)
        self.assertEqual(self.資料.著作所在地, self.臺灣)
        self.assertEqual(self.資料.著作年, self.一九五空年代)
        self.比較屬性(self.資料, self.句屬性)

    def test_屬性無合法的json字串(self):
        self.句內容['屬性'] = '{[}'
        self.assertRaises(ValueError, self.資料表.加資料, self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)

    def test_屬性是集合的json字串(self):
        self.句內容['屬性'] = '{"sui2"}'
        self.assertRaises(ValueError, self.資料表.加資料, self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)

    def test_屬性是字串的json字串(self):
        self.句內容['屬性'] = 'sui2'
        self.assertRaises(ValueError, self.資料表.加資料, self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)
    # 會當傳物件的攏用AttributeError

    def test_屬性是數字(self):
        self.句內容['屬性'] = 33
        with self.assertRaises(ValueError):
            self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)

    def test_屬性是字典(self):
        self.句內容['屬性'] = {'詞性'}
        with self.assertRaises(ValueError):
            self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)

    def test_屬性是陣列(self):
        self.句內容['屬性'] = ['詞性']
        with self.assertRaises(ValueError):
            self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)

    def test_屬性是集合(self):
        self.句內容['屬性'] = {'詞性'}
        with self.assertRaises(ValueError):
            self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)

    def test_無屬性(self):
        self.句內容.pop('屬性')
        原來資料數 = self.資料表.objects.all().count()
        資料 = self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 原來資料數 + 1)
        self.assertEqual(資料.收錄者, self.Pigu)
        self.assertEqual(資料.來源, self.鄉民)
        self.assertEqual(資料.版權, self.袂使公開)
        self.assertEqual(資料.種類, self.語句)
        self.assertEqual(資料.語言腔口, self.四縣話)
        self.assertEqual(資料.著作所在地, self.臺灣)
        self.assertEqual(資料.著作年, self.一九五空年代)
        self.比較屬性(資料, {})

    def test_濟个綜合語料(self):
        self.句內容['來源'] = json.dumps({'名': '阿媠', '職業': '學生'})
        self.句內容['版權'] = self.袂使公開.pk
        self.句內容['語言腔口'] = '豬豬語'
        self.句內容['著作所在地'] = '員林'
        原來資料數 = self.資料表.objects.all().count()
        資料 = self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 原來資料數 + 1)
        self.assertEqual(資料.收錄者, self.Pigu)
        self.assertEqual(資料.來源.名, '阿媠')
        self.assertEqual(資料.來源.屬性.count(), 1)
        self.assertEqual(資料.來源.屬性.first().分類, '職業')
        self.assertEqual(json.loads(資料.來源.屬性.first().性質), '學生')
        self.assertEqual(資料.來源.屬性.first().內容(), {'職業': '學生'})
        self.assertEqual(資料.版權, self.袂使公開)
        self.assertEqual(資料.種類, self.語句)
        self.assertEqual(資料.語言腔口.語言腔口, '豬豬語')
        self.assertEqual(資料.著作所在地.著作所在地, '員林')
        self.assertEqual(資料.著作年, self.一九五空年代)
        self.比較屬性(資料, self.句屬性)

    def test_規個內容用字串(self):
        self.詞內容 = json.dumps(self.詞內容)
        self.test_加詞()
        self.句內容 = json.dumps(self.句內容)
        self.test_加句()

    def 比較屬性(self, 資料, 屬性欄位內容):
        try:
            內容 = json.loads(屬性欄位內容)
        except Exception:
            內容 = 屬性欄位內容
        self.assertEqual(資料.屬性內容(), 內容)

    def test_來源仝名無仝屬性試驗(self):
        無屬性花蓮人 = 來源表.objects.create(名='Dr. Pigu')
        學生花蓮人 = 來源表.objects.create(名='Dr. Pigu')
        學生花蓮人.屬性.add(
            來源屬性表.objects.create(分類='職業', 性質='學生'),
        )

        self.詞內容['收錄者'] = {'名': 'Dr. Pigu', '出世地': '花蓮人'}
        self.assertRaises(ObjectDoesNotExist, self.資料表.加資料, self.詞內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)

        self.句內容['來源'] = {'名': 'Dr. Pigu', '出世地': '花蓮人'}
        原來資料數 = self.資料表.objects.all().count()
        self.資料 = self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 原來資料數 + 1)
        self.assertEqual(self.資料.收錄者, self.Pigu)
        self.assertNotEqual(self.資料.來源, self.Pigu)
        self.assertNotEqual(self.資料.來源, 無屬性花蓮人)
        self.assertNotEqual(self.資料.來源, 學生花蓮人)
        self.assertEqual(self.資料.來源.名, 'Dr. Pigu')
        self.assertEqual(self.資料.來源.屬性.count(), 1)
        self.assertEqual(self.資料.來源.屬性.first().分類, '出世地')
        self.assertEqual(json.loads(self.資料.來源.屬性.first().性質), '花蓮人')
        self.assertEqual(self.資料.來源.屬性.first().內容(), {'出世地': '花蓮人'})
        self.assertEqual(self.資料.版權, self.袂使公開)
        self.assertEqual(self.資料.種類, self.語句)
        self.assertEqual(self.資料.語言腔口, self.四縣話)
        self.assertEqual(self.資料.著作所在地, self.臺灣)
        self.assertEqual(self.資料.著作年, self.一九五空年代)
        self.比較屬性(self.資料, self.句屬性)

    def test_全部參數攏傳物件(self):
        self.句內容.update({
            '收錄者': self.Pigu,
            '來源': self.鄉民,
            '版權': self.袂使公開,
            '種類': self.語句,
            '語言腔口': self.四縣話,
            '著作所在地': self.臺灣,
            '著作年': self.一九五空年代,
        })
        self.test_加句()
