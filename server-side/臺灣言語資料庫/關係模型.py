# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.deletion import CASCADE
from 臺灣言語資料庫.資料模型 import 外語表
from 臺灣言語資料庫.資料模型 import 影音表
from 臺灣言語資料庫.資料模型 import 文本表
from 臺灣言語資料庫.資料模型 import 聽拍表


class 翻譯影音表(models.Model):
    外語 = models.ForeignKey(外語表, related_name='翻譯影音', on_delete=CASCADE)
    影音 = models.OneToOneField(影音表, related_name='來源外語', on_delete=CASCADE)

    def __str__(self):
        return '{}→{}'.format(self.外語, self.影音)


class 翻譯文本表(models.Model):
    外語 = models.ForeignKey(外語表, related_name='翻譯文本', on_delete=CASCADE)
    文本 = models.OneToOneField(文本表, related_name='來源外語', on_delete=CASCADE)

    def __str__(self):
        return '{}→{}'.format(self.外語, self.文本)


class 影音文本表(models.Model):
    影音 = models.ForeignKey(影音表, related_name='影音文本', on_delete=CASCADE)
    文本 = models.OneToOneField(文本表, related_name='來源影音', on_delete=CASCADE)

    def __str__(self):
        return '{}→{}'.format(self.影音, self.文本)


class 影音聽拍表(models.Model):
    影音 = models.ForeignKey(影音表, related_name='影音聽拍', on_delete=CASCADE)
    聽拍 = models.OneToOneField(聽拍表, related_name='+', on_delete=CASCADE)

    def __str__(self):
        return '{}→{}'.format(self.影音, self.聽拍)


class 文本校對表(models.Model):
    舊文本 = models.ForeignKey(文本表, related_name='文本校對', on_delete=CASCADE)
    新文本 = models.OneToOneField(文本表, related_name='來源校對資料', on_delete=CASCADE)

    def __str__(self):
        return '{}→{}'.format(self.舊文本, self.新文本)


class 聽拍校對表(models.Model):
    舊聽拍 = models.ForeignKey(聽拍表, related_name='聽拍校對', on_delete=CASCADE)
    新聽拍 = models.OneToOneField(聽拍表, related_name='來源校對資料', on_delete=CASCADE)

    def __str__(self):
        return '{}→{}'.format(self.舊聽拍, self.新聽拍)
