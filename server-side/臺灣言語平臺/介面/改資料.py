# -*- coding:utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.shortcuts import render


from 臺灣言語平臺.項目模型 import 平臺項目表
from 臺灣言語平臺.介面.Json失敗回應 import Json失敗回應
from 臺灣言語平臺.外語請教條 import 外語請教條


class 失敗的json回應(Json失敗回應):

    def __init__(self, 失敗原因):
        super(失敗的json回應, self).__init__({
            '錯誤': 失敗原因,
        })


class 成功的json回應(JsonResponse):

    def __init__(self, 平臺項目編號):
        super(成功的json回應, self).__init__({
            '平臺項目編號': str(平臺項目編號),
        })


@login_required
def 把測試資料藏起來_管理目錄(request):
    資料列表 = 外語請教條.無建議講法的外語表_管理頁面()[:300]

    資料 = []
    for data in 資料列表:
        編號 = data.平臺項目.編號()
        名稱 = data.平臺項目.資料()
        愛藏起來 = data.平臺項目.愛藏起來
        資料.append({
            '編號': 編號, '名稱': 名稱, '愛藏起來': 愛藏起來
        })

    return render(request, '藏我很會.html', {
        '資料': 資料,
    })


@login_required
def 把測試資料藏起來(request):
    try:
        資料編號 = int(request.POST['資料編號'].strip())
    except ValueError:
        return 失敗的json回應('資料編號只能是數字')
    平臺項目表.把無建議的外語資料藏起來(資料編號)
    return 成功的json回應(資料編號)
