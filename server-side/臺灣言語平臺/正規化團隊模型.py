from django.db import models
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from 臺灣言語資料庫.資料模型 import 語言腔口表
from 臺灣言語資料庫.關係模型 import 文本校對表
from 臺灣言語平臺.項目模型 import 平臺項目表
from django.core.exceptions import ValidationError


class 正規化sheet表(models.Model):
    google_sheet_scope = ['https://spreadsheets.google.com/feeds']

    語言腔口 = models.OneToOneField(
        語言腔口表, null=False, related_name='正規化sheet', on_delete=models.CASCADE
    )
    key_file_name = models.CharField(blank=False, max_length=200)
    url = models.CharField(unique=True, max_length=200)

    @classmethod
    def 加sheet(cls, 語言腔口, key_file_name, url):
        語言腔口物件 = 語言腔口表.objects.get_or_create(語言腔口=語言腔口)[0]
        return cls.objects.create(
            語言腔口=語言腔口物件,
            key_file_name=key_file_name,
            url=url
        )

    @classmethod
    def 全部整理到資料庫(cls):
        for sheet資料 in cls.全部資料():
            sheet資料.整理到資料庫()

    @classmethod
    def 全部資料(cls):
        return cls.objects.all()

    def 提著資料表(self):
        登入憑證 = ServiceAccountCredentials.from_json_keyfile_name(
            self.key_file_name, self.google_sheet_scope
        )
        return gspread.authorize(登入憑證).open_by_url(
            self.url
        ).sheet1

    @classmethod
    def 文本加入sheet(cls, 平臺項目編號):
        平臺項目 = 平臺項目表.揣編號(平臺項目編號)
        文本 = 平臺項目.資料()
        if 文本.文本校對.exists():
            return
        try:
            正規化sheet = 文本.語言腔口.正規化sheet
        except Exception:
            return
        資料表 = 正規化sheet.提著資料表()
        if cls._編號有佇表內底無(資料表, 平臺項目.編號()):
            return
        正規化sheet表.新文本自資料庫加入sheet(資料表, 平臺項目)

    @classmethod
    def _編號有佇表內底無(cls, 資料表, 編號):
        if str(編號) in 資料表.col_values(1)[1:]:
            return True
        return False

    @classmethod
    def _原本文本項目指去新的外語(cls, 原本平臺項目, 正確華語):
        舊外語項目編號 = 原本平臺項目.文本.來源外語.外語.平臺項目.編號()
        try:
            新外語項目 = 平臺項目表.加外語資料({'外語資料': 正確華語})
        except ValidationError as 錯誤:
            新外語項目 = 平臺項目表.揣編號(錯誤.平臺項目編號)
        來源外語 = 原本平臺項目.文本.來源外語
        來源外語.外語 = 新外語項目.外語
        來源外語.save()
        舊外語項目 = 平臺項目表.揣編號(舊外語項目編號)
        舊外語 = 舊外語項目.外語
        if not 舊外語.翻譯文本.exists() and not 舊外語.翻譯影音.exists():
            舊外語項目.delete()
            舊外語.delete()

    @staticmethod
    def _揣外語資料(文本):
        try:
            return 文本.來源外語.外語.外語資料
        except Exception:
            return 文本.來源影音.影音.來源外語.外語.外語資料

    def 整理到資料庫(self):
        資料表 = self.提著資料表()
        全部資料 = 資料表.get_all_values()
        標題 = 全部資料[0]
        for 一筆 in 全部資料[1:]:
            這筆資料 = dict(zip(標題, 一筆))
            正規化sheet表.正規化文本自sheet加轉資料庫(這筆資料)

    @staticmethod
    def 新文本自資料庫加入sheet(資料表, 平臺項目):
        文本 = 平臺項目.資料()
        音標 = 文本.音標資料
        資料表.append_row(
            [
                str(平臺項目.編號()), 文本.來源.名,
                正規化sheet表._揣外語資料(文本), 文本.文本資料, 音標,
                '', '', '',
                '', ''
            ]
        )

    @staticmethod
    def 正規化文本自sheet加轉資料庫(這筆資料):
        '若是有問題，就return None。無就回傳`平臺項目`'
        try:
            平臺項目編號 = int(這筆資料['流水號'])
            原本平臺項目 = 平臺項目表.揣編號(平臺項目編號)
            # 有匯入過資料就離開
            if 原本平臺項目.校對後的文本():
                return
        except 文本校對表.DoesNotExist:
            pass
        except 文本校對表.MultipleObjectsReturned:
            return
        except Exception:
            return
        外語 = 原本平臺項目.文本.來源外語.外語
        原華語 = 外語.外語資料
        原漢字 = 原本平臺項目.文本.文本資料
        原音標 = 原本平臺項目.文本.音標資料
        正確華語 = 這筆資料['正確華語'].strip()
        漢字 = 這筆資料['正規漢字'].strip()
        臺羅 = 這筆資料['臺羅'].strip()
        編輯者 = 這筆資料['編輯者(簽名)'].strip()
        if (漢字, 臺羅) in [(原漢字, 原音標)]:
            平臺項目 = 平臺項目表.揣編號(平臺項目編號)
            平臺項目.設為推薦用字()
            if 正確華語 != '' and 正確華語 != 原華語:
                正規化sheet表._原本文本項目指去新的外語(原本平臺項目, 正確華語)
            return 平臺項目
        elif 漢字 != '' and 臺羅 != '' and 編輯者 != '':
            平臺項目 = 平臺項目表.對正規化sheet校對母語文本(
                平臺項目編號,
                編輯者,
                漢字,
                臺羅,
            )
            if 正確華語 != '' and 正確華語 != 原華語:
                正規化sheet表._原本文本項目指去新的外語(原本平臺項目, 正確華語)
            return 平臺項目
        return
