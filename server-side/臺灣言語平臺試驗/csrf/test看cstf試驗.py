# -*- coding: utf-8 -*-
from django.test import TestCase
import json


class 看csrf試驗(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_有csrftoken(self):
        回應 = self.client.get('/csrf/看')
# 		前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertIn('csrftoken', 回應資料)

    def test_csrftoken長度(self):
        回應 = self.client.get('/csrf/看')
# 		前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertIn(len(回應資料['csrftoken']), [32, 64])
