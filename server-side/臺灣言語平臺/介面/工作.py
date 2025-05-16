from django.http.response import HttpResponseRedirect

from 臺灣言語平臺.tasks import 半瞑自sheets掠轉資料庫


def 正規化表馬上匯入資料庫(request):
    半瞑自sheets掠轉資料庫.delay()
    return HttpResponseRedirect('https://itaigi.tw')
