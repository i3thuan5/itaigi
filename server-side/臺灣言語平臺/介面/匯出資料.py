# -*- coding:utf-8 -*-
from django.http.response import JsonResponse

from 臺灣言語資料庫.關係模型 import 文本校對表
from 臺灣言語資料庫.資料模型 import 文本表


def 匯出辭典資料(_request):
    資料 = []
    for 文本, 來源, 華語 in _揣出會使的資料():
        資料.append({
            '華語': 華語.外語資料,
            '來源': 來源,
            '漢字': 文本.文本資料,
            '羅馬字': 文本.音標資料,
        })
    return JsonResponse({'資料': 資料})


def _揣出會使的資料():
    for 文本校對 in (
        文本校對表.objects
        .prefetch_related('新文本', '舊文本__來源', '舊文本__來源外語__外語')
    ):
        yield 文本校對.新文本, 文本校對.舊文本.來源.名, 文本校對.舊文本.來源外語.外語
    for 文本 in (
        文本表.objects
        .filter(平臺項目__推薦用字=True, 來源校對資料__isnull=True)
        .prefetch_related('來源', '來源外語__外語')
    ):
        yield 文本, 文本.來源.名, 文本.來源外語.外語
