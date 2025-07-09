from django.http.response import JsonResponse


def 登入狀況(request):
    if request.user.is_authenticated:
        return JsonResponse({'使用者編號': str(request.user.編號())})
    return JsonResponse({'使用者編號': '無登入'})
