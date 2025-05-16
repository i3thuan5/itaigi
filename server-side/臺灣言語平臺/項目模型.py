# -*- coding: utf-8 -*-
import json

from django.conf import settings
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models
from django.db.models import F
from django.utils import timezone


from 臺灣言語資料庫.資料模型 import 外語表
from 臺灣言語資料庫.資料模型 import 影音表
from 臺灣言語資料庫.資料模型 import 文本表
from 臺灣言語資料庫.資料模型 import 聽拍表
from 臺灣言語資料庫.資料模型 import 種類表
from 臺灣言語資料庫.資料模型 import 語言腔口表
from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語資料庫.欄位資訊 import 字詞


class 平臺項目表(models.Model):
    項目名 = '平臺項目'
    外語 = models.OneToOneField(
        外語表, null=True, related_name=項目名, on_delete=models.CASCADE
    )
    影音 = models.OneToOneField(
        影音表, null=True, related_name=項目名, on_delete=models.CASCADE
    )
    文本 = models.OneToOneField(
        文本表, null=True, related_name=項目名, on_delete=models.CASCADE
    )
    聽拍 = models.OneToOneField(
        聽拍表, null=True, related_name=項目名, on_delete=models.CASCADE
    )
    推薦用字 = models.BooleanField(default=False)
    按呢講好 = models.IntegerField(default=0)
    按呢無好 = models.IntegerField(default=0)
    # When value is False, then data will be visible
    愛藏起來 = models.BooleanField(default=False)
    保存時間 = models.DateTimeField(auto_now=True)
    查幾擺 = models.IntegerField(default=1)

    def __str__(self):
        try:
            return '華語：' + self.外語.外語資料
        except Exception:
            return '台語：' + self.文本.文本資料

    def 編號(self):
        return self.pk

    @classmethod
    def 揣編號(cls, 編號):
        return cls.objects.get(pk=編號)

    def 資料(self):
        結果 = []
        if self.外語:
            結果.append(self.外語)
        if self.影音:
            結果.append(self.影音)
        if self.文本:
            結果.append(self.文本)
        if self.聽拍:
            結果.append(self.聽拍)
        if len(結果) == 1:
            return 結果[0]
        if len(結果) == 0:
            raise RuntimeError('平臺項目無指向任何一个物件')
        raise RuntimeError('平臺項目指向兩个以上物件')

    @classmethod
    def 加外語資料(cls, 內容):
        try:
            原本外語 = cls._找外語資料(內容)
            錯誤 = ValidationError('已經有相同的外語資料了')
            錯誤.平臺項目編號 = 原本外語.編號()
            raise 錯誤
        except ObjectDoesNotExist:
            pass
        外語 = 外語表.加資料(cls._補預設欄位(內容, 字詞))
        return cls.objects.create(外語=外語)

    @classmethod
    def _找外語資料(cls, 內容):
        要求 = 外語表.objects.filter(外語資料=內容['外語資料'])
        try:
            要求 = 要求.filter(種類=種類表.objects.get(種類=內容['種類']))
        except ObjectDoesNotExist:
            要求 = 要求.none()
        except Exception:
            pass
        try:
            要求 = 要求.filter(語言腔口表.objects.get(語言腔口=內容['語言腔口']))
        except ObjectDoesNotExist:
            要求 = 要求.none()
        except Exception:
            pass
        try:
            要求 = 要求.filter(語言腔口表.objects.get(語言腔口=內容['外語語言']))
        except ObjectDoesNotExist:
            要求 = 要求.none()
        except Exception:
            pass
        return 要求.get().平臺項目

    @classmethod
    def 把無建議的外語資料藏起來(cls, 編號):
        hangbok = cls.objects.get(pk=編號)
        hangbok.愛藏起來 = not hangbok.愛藏起來
        hangbok.save()
        return hangbok

    @classmethod
    def 外語錄母語(cls, 外語請教條項目編號, 內容):
        外語 = 平臺項目表.objects.get(pk=外語請教條項目編號).外語
        影音 = 外語.錄母語(cls._補預設欄位(內容, 外語.種類.種類))
        return cls.objects.create(影音=影音)

    @classmethod
    def 影音寫文本(cls, 新詞影音項目編號, 內容):
        影音 = 平臺項目表.objects.get(pk=新詞影音項目編號).影音
        文本 = 影音.寫文本(cls._補預設欄位(內容, 影音.種類.種類))
        return cls.objects.create(文本=文本)

    @classmethod
    def 外語翻母語(cls, 外語請教條項目編號, 內容):
        外語 = 平臺項目表.objects.get(pk=外語請教條項目編號).外語
        文本 = 外語.翻母語(cls._補預設欄位(內容, 外語.種類.種類))
        return cls.objects.create(文本=文本)

    @classmethod
    def 對正規化sheet校對母語文本(cls, 文本項目編號, 編輯者, 新文本, 新音標):
        舊文本項目 = 平臺項目表.objects.get(pk=文本項目編號)
        舊文本項目.取消推薦用字()
        舊文本物件 = 舊文本項目.資料()
        新文本內容 = {
            '收錄者': 來源表.objects.get_or_create(名='系統管理者')[0],
            '種類': 舊文本物件.種類.種類,
            '語言腔口': 舊文本物件.語言腔口.語言腔口,
            '文本資料': 新文本,
        }
        資料庫內底的來源 = 來源表.objects.filter(
            名=編輯者, 使用者__isnull=True, 屬性__isnull=True
        ).first()
        if 資料庫內底的來源 is not None:
            新文本內容['來源'] = 資料庫內底的來源
        else:
            新文本內容['來源'] = 來源表.加來源({'名': 編輯者})
        if 新音標:
            新文本內容['屬性'] = json.dumps({'音標': 新音標})
        新文本項目 = cls._校對母語文本(文本項目編號, 新文本內容)
        新文本項目.設為推薦用字()
        return 新文本項目

    @classmethod
    def _校對母語文本(cls, 文本項目編號, 內容):
        舊文本 = 平臺項目表.objects.get(pk=文本項目編號).文本
        新文本 = 舊文本.校對做(cls._補預設欄位(內容, 舊文本.種類.種類))
        return cls.objects.create(文本=新文本)

    def 校對後的文本(self):
        return self.資料().文本校對.get().新文本.平臺項目

    def 是推薦用字(self):
        return self.推薦用字

    def 設為推薦用字(self):
        self.推薦用字 = True
        self.save()

    def 取消推薦用字(self):
        self.推薦用字 = False
        self.save()

    def 有人查一擺(self):
        self.查幾擺 += 1
        self.save()

    @classmethod
    def 這句講了按怎(cls, 平臺項目編號, decision):
        if decision == '按呢講好':
            return (
                平臺項目表.objects
                .filter(pk=平臺項目編號)
                .update(按呢講好=F('按呢講好') + 1)
            )
        elif decision == '按呢無好':
            return (
                平臺項目表.objects
                .filter(pk=平臺項目編號)
                .update(按呢無好=F('按呢無好') + 1)
            )
        else:
            raise ValueError('decision傳毋著')

    @classmethod
    def _補預設欄位(cls, 內容, 種類):
        新內容 = {
            '收錄者': 來源表.objects.get(名='匿名').編號(),
            '來源': cls._自己json字串[0],
            '版權': '會使公開',
            '種類': 種類,
            '語言腔口': settings.MOTHER_TONGUE,
            '著作所在地': '臺灣',
            '著作年': str(timezone.now().year),
            '屬性': {},
            '外語語言': settings.FOREIGN_LANGUAGE,

        }
        新內容.update(內容)
        if cls.內容是自己的json字串(新內容):
            新內容['來源'] = 新內容['收錄者']
        return 新內容

    _自己 = '自己'
    _自己json字串 = [json.dumps(_自己), json.dumps(_自己, ensure_ascii=False)]

    @classmethod
    def 內容是自己的json字串(cls, 內容):
        if 內容['來源'] in cls._自己json字串:
            return True
        return False
