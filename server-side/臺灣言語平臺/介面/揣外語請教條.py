from django.http.response import JsonResponse


from 臺灣言語平臺.介面.Json失敗回應 import Json失敗回應
from 臺灣言語平臺.外語請教條 import 外語請教條
from django.conf import settings
from django.utils.datastructures import MultiValueDictKeyError


def 揣外語請教條(request):
    try:
        外語資料 = request.GET['關鍵字']
    except KeyError:
        return Json失敗回應({'錯誤': '無傳關鍵字'})

    符合資料 = []

    for 外語 in 外語請教條.有建議講法的外語表().filter(外語資料=外語資料):
        符合資料.append({
            '外語項目編號': str(外語.平臺項目.編號()),
            '外語資料': 外語.外語資料,
            '新詞文本': 外語.揣新詞文本(),
        })

    其他建議資料 = 外語請教條.揣其他建議資料(外語資料, settings.KIANGI_MAX)
    return JsonResponse({'列表': 符合資料, '其他建議': 其他建議資料})


def 揣無建議的外語(request):
    try:
        if request.GET['排序'] == 'new':
            照排 = ['-平臺項目__保存時間', '-pk']
        else:
            照排 = ['-平臺項目__查幾擺', '-pk']
    except MultiValueDictKeyError:
        照排 = ['-平臺項目__查幾擺', '-pk']
    符合資料 = []
    無建議的華語數量 = getattr(settings, 'BOKIANGI_HUAGI_MAX', 90)
    符合資料 = list(
        外語請教條.無建議講法的外語表(照排, 無建議的華語數量)
        .values_list('外語資料', flat=True))
    return JsonResponse({'列表': 符合資料})


def 揣按呢講外語請教條(request):
    try:
        關鍵字 = request.GET['關鍵字']
    except KeyError:
        return Json失敗回應({'錯誤': '無傳關鍵字'})
    符合資料 = []
    for 外語 in 外語請教條.有按呢講法的外語表(關鍵字):
        符合資料.append({
            '外語項目編號': str(外語.平臺項目.編號()),
            '外語資料': 外語.外語資料,
        })
    return JsonResponse({'列表': 符合資料})


def 揣上新貢獻的外語請教條(request):
    符合資料 = []
    for 外語 in 外語請教條.揣上新貢獻()[:100]:
        符合資料.append({
            '外語項目編號': str(外語.平臺項目.編號()),
            '外語資料': 外語.外語資料,
        })
    return JsonResponse({'列表': 符合資料})
