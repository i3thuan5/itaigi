# -*- coding: utf-8 -*-
from django.urls.base import resolve
from django.test import TestCase


from 臺灣言語平臺.使用者模型 import 使用者表
from 臺灣言語平臺.介面.登出入 import 登入狀況


class 登入狀況試驗(TestCase):

    def test_對應函式(self):
        對應 = resolve('/使用者/看編號')
        self.assertEqual(對應.func, 登入狀況)

    def test_無登入(self):
        self.client.logout()
        回應 = self.client.get('/使用者/看編號')

        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['使用者編號'], '無登入',)

    def test_一般使用者(self):
        阿媠 = 使用者表.加使用者(
            'sui2@pigu.tw', {"名": '阿媠', '出世年': '1950', '出世地': '臺灣', },
        )
        阿媠.set_password('sui2')
        阿媠.save()
        self.client.force_login(阿媠)

        回應 = self.client.get('/使用者/看編號')

        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['使用者編號'], str(阿媠.編號()),)
