from django.http.response import JsonResponse
from django.middleware.csrf import get_token


def 看csrf(request):
    return JsonResponse({'csrftoken': get_token(request)})
