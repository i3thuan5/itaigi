# -*- coding: utf-8 -*-
import io
import wave


class 加關係試驗:
    fixtures = ['試驗基本資料.yaml']

    def 加初始資料(self):
        self.詞檔案 = io.BytesIO()
        音檔 = wave.open(self.詞檔案, 'wb')
        音檔.setnchannels(1)
        音檔.setframerate(16000)
        音檔.setsampwidth(2)
        音檔.writeframesraw(b'0' * 100)
        音檔.close()
        self.句檔案 = io.BytesIO()
        音檔 = wave.open(self.句檔案, 'wb')
        音檔.setnchannels(1)
        音檔.setframerate(16000)
        音檔.setsampwidth(2)
        音檔.writeframesraw(b'0' * 100)
        音檔.close()

    def tearDown(self):
        self.詞檔案.close()
        self.句檔案.close()

    def test_加詞(self):
        原本資料 = self.原本資料表.加資料(self.原本資料詞內容)
        self.加詞(原本資料)

    def test_加句(self):
        原本資料 = self.原本資料表.加資料(self.原本資料句內容)
        self.加句(原本資料)

    def test_濟个正常語料(self):
        原本資料詞 = self.原本資料表.加資料(self.原本資料詞內容)
        self.加詞(原本資料詞)
        原本資料句 = self.原本資料表.加資料(self.原本資料句內容)
        self.加句(原本資料句)
        self.加句(原本資料句)
        self.加詞(原本資料詞)
        self.加詞(原本資料詞)
        self.加句(原本資料句)
        原本資料句 = self.原本資料表.加資料(self.原本資料句內容)
        self.加句(原本資料句)

    def test_無仝種類(self):
        原本資料詞 = self.原本資料表.加資料(self.原本資料詞內容)
        原本資料句 = self.原本資料表.加資料(self.原本資料句內容)
        self.對應資料詞內容['種類'] = '語句'
        self.對應資料句內容['種類'] = '字詞'
        self.assertRaises(ValueError, self.加詞, 原本資料詞)
        self.assertRaises(ValueError, self.加句, 原本資料句)

    def test_無種類(self):
        原本資料詞 = self.原本資料表.加資料(self.原本資料詞內容)
        原本資料句 = self.原本資料表.加資料(self.原本資料句內容)
        self.對應資料詞內容.pop('種類')
        self.對應資料句內容.pop('種類')
        self.assertRaises(KeyError, self.加詞, 原本資料詞)
        self.assertRaises(KeyError, self.加句, 原本資料句)

    def test_無仝語言腔口(self):
        原本資料詞 = self.原本資料表.加資料(self.原本資料詞內容)
        原本資料句 = self.原本資料表.加資料(self.原本資料句內容)
        self.對應資料詞內容['語言腔口'] = '泰雅話'
        self.對應資料句內容['語言腔口'] = '泰雅話'
        self.assertRaises(ValueError, self.加詞, 原本資料詞)
        self.assertRaises(ValueError, self.加句, 原本資料句)

    def test_無語言腔口(self):
        原本資料詞 = self.原本資料表.加資料(self.原本資料詞內容)
        原本資料句 = self.原本資料表.加資料(self.原本資料句內容)
        self.對應資料詞內容.pop('語言腔口')
        self.對應資料句內容.pop('語言腔口')
        self.assertRaises(KeyError, self.加詞, 原本資料詞)
        self.assertRaises(KeyError, self.加句, 原本資料句)

    def test_無仝種類佮語言腔口(self):
        原本資料詞 = self.原本資料表.加資料(self.原本資料詞內容)
        原本資料句 = self.原本資料表.加資料(self.原本資料句內容)
        self.assertRaises(ValueError, self.加詞, 原本資料句)
        self.assertRaises(ValueError, self.加句, 原本資料詞)
