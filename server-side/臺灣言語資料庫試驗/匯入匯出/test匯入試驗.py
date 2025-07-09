from django.test.testcases import TestCase
from os.path import dirname, abspath, join
from unittest.mock import patch, call


from 臺灣言語資料庫.資料模型 import 文本表
from 臺灣言語資料庫.匯出入 import 匯出入工具
from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語資料庫.資料模型 import 外語表
from 臺灣言語資料庫.資料模型 import 影音表


class 匯入試驗(TestCase):

    def setUp(self):
        self.匯入工具 = 匯出入工具()

    @patch('臺灣言語資料庫.資料模型.文本表.加資料')
    def test_下層攏愛做著(self, 加資料mocka):
        self.匯入工具.匯入檔案(self._提yaml資料('異用字.yaml'))
        self.assertEqual(加資料mocka.call_count, 2)

    @patch('臺灣言語資料庫.資料模型.文本表.加資料')
    def test_文本資料(self, 加資料mocka):
        self.匯入工具.匯入檔案(self._提yaml資料('異用字.yaml'))
        加資料mocka.assert_has_calls([
            call({
                '收錄者': 來源表.objects.get(名='系統管理者'),
                '來源': {'名': '教育部閩南語辭典'},
                '版權': '姓名標示-禁止改作 3.0 台灣',
                '種類': '字詞',
                '著作年': '2015',
                '著作所在地': '臺灣',
                '語言腔口': '閩南語',
                '文本資料': '蜀',
            }),
            call({
                '收錄者': 來源表.objects.get(名='系統管理者'),
                '來源': {'名': '教育部閩南語辭典'},
                '版權': '姓名標示-禁止改作 3.0 台灣',
                '種類': '字詞',
                '著作年': '2015',
                '著作所在地': '臺灣',
                '語言腔口': '閩南語',
                '文本資料': '落翅仔',
            }),
        ], any_order=True)

    @patch('臺灣言語資料庫.資料模型.文本表.校對做')
    def test_文本資料校對數量(self, 校對做mocka):
        self.匯入工具.匯入檔案(self._提yaml資料('異用字.yaml'))
        self.assertGreaterEqual(校對做mocka.call_count, 2)

    def test_文本資料校對資料(self):
        self.匯入工具.匯入檔案(self._提yaml資料('異用字.yaml'))
        self.assertEqual(文本表.objects.filter(文本資料='一').count(), 1)
        self.assertEqual(文本表.objects.filter(文本資料='落翼仔').count(), 2)

    @patch('臺灣言語資料庫.資料模型.外語表.加資料')
    def test_外語資料(self, 加資料mocka):
        self.匯入工具.匯入檔案(self._提yaml資料('xls整理.yaml'))
        加資料mocka.assert_called_once_with({
            '收錄者': 來源表.objects.get(名='系統管理者'),
            '來源': {'名': '教育部閩南語辭典'},
            '版權': '姓名標示-禁止改作 3.0 台灣',
            '種類': '語句',
            '著作年': '2015',
            '著作所在地': '臺灣',
            '語言腔口': '閩南語',
            '外語語言': '華語',
            '外語資料': '鼓膜破了。',
        })

    @patch('臺灣言語資料庫.資料模型.外語表.翻母語')
    def test_翻母語(self, 翻母語mocka):
        self.匯入工具.匯入檔案(self._提yaml資料('xls整理.yaml'))
        翻母語mocka.assert_called_once_with({
            '收錄者': 來源表.objects.get(名='系統管理者'),
            '來源': {'名': '教育部閩南語辭典'},
            '版權': '姓名標示-禁止改作 3.0 台灣',
            '種類': '語句',
            '著作年': '2015',
            '著作所在地': '臺灣',
            '語言腔口': '閩南語',
            '文本資料': '耳鏡破去矣。',
            '屬性': {'音標': 'hinn7-kiann3 phua3-0khi3-0ah4 .'}
        })

    def test_翻母語濟層語料(self):
        self.匯入工具.匯入檔案(self._提yaml資料('xls整理.yaml'))
        self.assertEqual(文本表.objects.filter(文本資料='耳鏡破去矣。').count(), 1)

    def test_翻母語相關資料語料(self):
        self.匯入工具.匯入檔案(self._提yaml資料('掃街變成來亂的.yaml'))
        外語 = 外語表.objects.get()
        self.assertEqual(外語.外語資料, '今天生意好嗎!?')
        網路文本 = 外語.翻譯文本.get().文本
        self.assertEqual(網路文本.文本資料, '今仔日生意干好!?')
        校對文本 = 網路文本.文本校對.get().新文本
        self.assertEqual(校對文本.文本資料, '今仔日生意敢好!?')

    @patch('臺灣言語資料庫.資料模型.影音表.加資料')
    def test_孤影音檔案加資料(self, 加資料mocka):
        self.匯入工具.匯入檔案(self._提yaml資料('孤影音.yaml'))
        self.assertEqual(加資料mocka.call_count, 1)

    def test_孤影音檔案有成功(self):
        self.assertEqual(影音表.objects.all().count(), 0)
        self.匯入工具.匯入檔案(self._提yaml資料('孤影音.yaml'))
        self.assertEqual(影音表.objects.all().count(), 1)

    @patch('臺灣言語資料庫.資料模型.外語表.錄母語')
    def test_影音檔案錄母語(self, 錄母語mocka):
        self.匯入工具.匯入檔案(self._提yaml資料('影音檔案.yaml'))
        self.assertEqual(錄母語mocka.call_count, 1)

    def test_影音檔案有文本(self):
        self.匯入工具.匯入檔案(self._提yaml資料('影音檔案.yaml'))
        self.assertEqual(文本表.objects.all().count(), 2)

    @patch('臺灣言語資料庫.資料模型.外語表.錄母語')
    def test_無用影音錄母語(self, 錄母語mocka):
        self.匯入工具.匯入檔案(self._提yaml資料('影音檔案.yaml'), 匯入影音=False)
        self.assertEqual(錄母語mocka.call_count, 0)

    @patch('臺灣言語資料庫.資料模型.影音表.加資料')
    def test_無用影音加資料(self, 加資料mocka):
        self.匯入工具.匯入檔案(self._提yaml資料('影音檔案.yaml'), 匯入影音=False)
        self.assertEqual(加資料mocka.call_count, 0)

    def test_無用影音有文本(self):
        self.匯入工具.匯入檔案(self._提yaml資料('影音檔案.yaml'), 匯入影音=False)
        self.assertEqual(文本表.objects.all().count(), 2)

    @patch('臺灣言語資料庫.資料模型.外語表.加資料')
    def test_全部相關資料組外語表加資料(self, 加資料mocka):
        self.匯入工具.匯入檔案(self._提yaml資料('全部相關資料組.yaml'))
        加資料mocka.assert_called_once_with({
            '收錄者': 來源表.objects.get(名='系統管理者'),
            '來源': {'名': '教育部閩南語辭典'},
            '版權': '姓名標示-禁止改作 3.0 台灣',
            '種類': '字詞',
            '著作年': '2015',
            '著作所在地': '臺灣',
            '語言腔口': '閩南語',
            '外語語言': '華語',
            '外語資料': '美麗',
        })

    @patch('臺灣言語資料庫.資料模型.外語表.錄母語')
    def test_全部相關資料組外語表錄母語(self, 錄母語mocka):
        self.匯入工具.匯入檔案(self._提yaml資料('全部相關資料組.yaml'))
        錄母語mocka.assert_called_once_with({
            '收錄者': 來源表.objects.get(名='系統管理者'),
            '來源': {'名': '教育部閩南語辭典'},
            '版權': '姓名標示-禁止改作 3.0 台灣',
            '種類': '字詞',
            '著作年': '2015',
            '著作所在地': '臺灣',
            '語言腔口': '閩南語',
            '影音所在': join(dirname(abspath(__file__)), '資料', 'audio', '08345.mp3'),
        })

    @patch('臺灣言語資料庫.資料模型.影音表.寫文本')
    def test_全部相關資料組影音表寫文本(self, 寫文本mocka):
        self.匯入工具.匯入檔案(self._提yaml資料('全部相關資料組.yaml'))
        寫文本mocka.assert_called_once_with({
            '收錄者': 來源表.objects.get(名='系統管理者'),
            '來源': {'名': '教育部閩南語辭典'},
            '版權': '姓名標示-禁止改作 3.0 台灣',
            '種類': '字詞',
            '著作年': '2015',
            '著作所在地': '臺灣',
            '語言腔口': '閩南語',
            '文本資料': '媠噹噹',
            '屬性': {'音標': 'hinn7-kiann3 phua3-0khi3-0ah4 .'}
        })

    def _提yaml資料(self, 檔名):
        return join(dirname(abspath(__file__)), '資料', 檔名)
