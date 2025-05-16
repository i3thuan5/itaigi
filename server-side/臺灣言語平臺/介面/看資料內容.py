from dateutil import tz
from django.http.response import JsonResponse


from 臺灣言語平臺.項目模型 import 平臺項目表

from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語平臺.介面.Json失敗回應 import Json失敗回應
from django.core.exceptions import ObjectDoesNotExist

_臺北時間 = tz.gettz('Asia/Taipei')
_時間輸出樣式 = '%Y-%m-%d %H:%M:%S'


def 轉做臺北時間字串(時間物件):
    return 時間物件.astimezone(_臺北時間).strftime(_時間輸出樣式)


def 看資料詳細內容(request):
    try:
        平臺項目編號 = request.GET['平臺項目編號']
    except KeyError:
        return Json失敗回應({'錯誤': '沒有平臺項目的編號'})
    try:
        平臺項目 = 平臺項目表.揣編號(int(平臺項目編號))
        資料 = 平臺項目.資料()
    except ObjectDoesNotExist:
        return Json失敗回應({'錯誤': '這不是合法平臺項目的編號'})
    return JsonResponse({
        '收錄者': str(資料.收錄者.編號()),
        '來源': str(資料.來源.編號()),
        '收錄時間': 轉做臺北時間字串(資料.收錄時間),
        '種類': 資料.種類.種類,
        '語言腔口': 資料.語言腔口.語言腔口,
        '版權': 資料.版權.版權,
        '著作所在地': 資料.著作所在地.著作所在地,
        '著作年': 資料.著作年.著作年,
        '屬性內容': 資料.屬性內容(),
        '按呢講好': 平臺項目.按呢講好,
        '按呢無好': 平臺項目.按呢無好
    })


def 看來源內容(request):
    try:
        來源編號 = request.GET['來源編號']
    except KeyError:
        return Json失敗回應({'錯誤': '沒有來源編號的參數'})
    try:
        來源 = 來源表.objects.get(pk=來源編號)
    except ObjectDoesNotExist:
        return Json失敗回應({'錯誤': '這不是合法的來源編號'})
    來源內容 = {
        '名': 來源.名,
        '屬性內容': 來源.屬性內容(),
    }
    try:
        來源內容['email'] = 來源.使用者.email
        來源內容['分數'] = 來源.使用者.分數
    except Exception:
        pass
    return JsonResponse(來源內容)


def 投票(request):
    try:
        平臺項目編號 = request.POST['平臺項目編號']
        decision = request.POST['decision']
    except KeyError:
        return Json失敗回應({'錯誤': '沒有平臺項目的編號'})
    try:
        rows_affect = 平臺項目表.這句講了按怎(平臺項目編號, decision)
    except ValueError:
        return Json失敗回應({'錯誤': 'decision傳錯了'})
    return JsonResponse({
        'suId': 平臺項目編號,
        'success': True if rows_affect == 1 else False,
    })
