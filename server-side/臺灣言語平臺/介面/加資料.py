# -*- coding:utf-8 -*-
import json

from django.core.exceptions import ValidationError
from django.http.response import JsonResponse
from django.utils.datastructures import MultiValueDictKeyError


from 臺灣言語資料庫.資料模型 import 種類表
from 臺灣言語平臺.項目模型 import 平臺項目表
from 臺灣言語平臺.介面.Json失敗回應 import Json失敗回應
from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語平臺.tasks import 新文本自資料庫加入sheet


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


def 加文本了愛加入sheet(介面函式):
    def 包起來(參數):
        json回應 = 介面函式(參數)
        try:
            平臺項目編號 = json.loads(json回應.content.decode('utf-8'))['平臺項目編號']
            新文本自資料庫加入sheet.delay(平臺項目編號)
        except KeyError:
            pass
        return json回應
    return 包起來


def 加外語請教條(request):
    欄位表 = [
        '來源',
        '種類',
        '語言腔口',
        '著作所在地',
        '著作年',
        '屬性',
        '外語語言',
    ]
    內容 = {}
    try:
        內容['收錄者'] = request.user.來源
    except Exception:
        內容['收錄者'] = 來源表.objects.get(名='匿名')

    for 欄位 in 欄位表:
        try:
            內容[欄位] = request.POST[欄位]
        except KeyError:
            pass
    try:
        內容['外語資料'] = request.POST['外語資料'].strip()
    except MultiValueDictKeyError:
        return 失敗的json回應('資料欄位有缺')

    try:
        平臺項目 = 平臺項目表.加外語資料(內容)
    except ValueError:
        return 失敗的json回應('來源抑是屬性無轉json字串')
    except KeyError:
        return 失敗的json回應('來源沒有「名」的欄位')
    except 種類表.DoesNotExist:
        return 失敗的json回應('種類欄位不符規範')
    except ValidationError as 錯誤:
        更新時間戳 = 平臺項目表.揣編號(編號=錯誤.平臺項目編號)
        更新時間戳.有人查一擺()
        return JsonResponse({
            '其他': '這個外語已經有了',
            '平臺項目編號': str(錯誤.平臺項目編號),
        })
    else:
        return 成功的json回應(平臺項目.編號())


def 加新詞影音(request):
    if '影音資料' in request.POST:
        return 失敗的json回應('影音資料不是檔案')
    欄位表 = [
        '來源',
        '種類',
        '語言腔口',
        '著作所在地',
        '著作年',
        '屬性',
    ]
    內容 = {}
    try:
        內容['收錄者'] = request.user.來源
    except Exception:
        內容['收錄者'] = 來源表.objects.get(名='匿名')
    for 欄位 in 欄位表:
        try:
            內容[欄位] = request.POST[欄位]
        except KeyError:
            pass
    try:
        內容['影音資料'] = request.FILES['影音資料']
        外語項目編號 = int(request.POST['外語項目編號'])
    except MultiValueDictKeyError:
        return 失敗的json回應('資料欄位有缺')
    except ValueError:
        return 失敗的json回應('編號欄位不是數字字串')

    try:
        平臺項目 = 平臺項目表.外語錄母語(外語項目編號, 內容)
    except ValueError as 錯誤:
        錯誤資訊 = 錯誤.args[0]
        if '新資料的種類' in 錯誤資訊 and '原本資料的種類' in 錯誤資訊:
            return 失敗的json回應('種類和外語不一樣')
        elif '新資料的語言腔口' in 錯誤資訊 and '原本資料的語言腔口' in 錯誤資訊:
            return 失敗的json回應('語言腔口和外語不一樣')
        else:
            return 失敗的json回應('來源抑是屬性無轉json字串')
    except KeyError:
        return 失敗的json回應('來源沒有「名」的欄位')
    except 平臺項目表.DoesNotExist:
        return 失敗的json回應('編號號碼有問題')
    except OSError:
        return 失敗的json回應('影音資料不是影音檔案')
    else:
        return 成功的json回應(平臺項目.編號())


@加文本了愛加入sheet
def 外語加新詞文本(request):
    欄位表 = [
        '來源',
        '種類',
        '語言腔口',
        '著作所在地',
        '著作年',
        '屬性',
    ]
    內容 = {'屬性': {}}
    try:
        內容['收錄者'] = request.user.來源
    except Exception:
        內容['收錄者'] = 來源表.objects.get(名='匿名')

    for 欄位 in 欄位表:
        try:
            內容[欄位] = request.POST[欄位]
        except KeyError:
            pass
    try:
        內容['屬性']['音標'] = request.POST['音標資料'].strip()
    except KeyError:
        pass
    try:
        內容['文本資料'] = request.POST['文本資料'].strip()
        外語項目編號 = int(request.POST['外語項目編號'])
    except MultiValueDictKeyError:
        return 失敗的json回應('資料欄位有缺')
    except ValueError:
        return 失敗的json回應('編號欄位不是數字字串')

    try:
        平臺項目 = 平臺項目表.外語翻母語(外語項目編號, 內容)
    except ValueError as 錯誤:
        錯誤資訊 = 錯誤.args[0]
        if '新資料的種類' in 錯誤資訊 and '原本資料的種類' in 錯誤資訊:
            return 失敗的json回應('種類和外語不一樣')
        elif '新資料的語言腔口' in 錯誤資訊 and '原本資料的語言腔口' in 錯誤資訊:
            return 失敗的json回應('語言腔口和外語不一樣')
        else:
            return 失敗的json回應('來源抑是屬性無轉json字串')
    except KeyError:
        return 失敗的json回應('來源沒有「名」的欄位')
    except 平臺項目表.DoesNotExist:
        return 失敗的json回應('編號號碼有問題')
    else:
        return 成功的json回應(平臺項目.編號())
