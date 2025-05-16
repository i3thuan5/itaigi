# -*- coding:utf-8 -*-
from django.http.response import HttpResponseBadRequest
import json


class Json失敗回應(HttpResponseBadRequest):

    def __init__(self, 回應資料):
        super(Json失敗回應, self).__init__(json.dumps(回應資料))
