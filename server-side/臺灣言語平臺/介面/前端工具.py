from django.http.response import HttpResponsePermanentRedirect


def 重導向前端(request):
    全部網址 = request.GET['網址']
    for 參數, 內容 in request.GET.items():
        if 參數 != '網址':
            全部網址 += '&{}={}'.format(參數, 內容)
    return HttpResponsePermanentRedirect(全部網址)
