from django.http.response import HttpResponsePermanentRedirect
from django.test.testcases import TestCase


class 重導向前端試驗(TestCase):

    def test_有導向(self):
        回應 = self.client.get(
            '/導向',
            {'網址': 'http://itaigi.tw'}
        )
        self.assertEqual(回應.status_code, 301)

    def test_是導向(self):
        回應 = self.client.get(
            '/導向',
            {'網址': 'http://itaigi.tw'}
        )
        self.assertIsInstance(回應, HttpResponsePermanentRedirect)

    def test_檢查網址(self):
        回應 = self.client.get(
            '/導向',
            {'網址': 'http://itaigi.tw'}
        )
        self.assertEqual(回應.url, 'http://itaigi.tw')

    def test_檢查網址有參數(self):
        回應 = self.client.get(
            '/導向',
            {
                '網址':
                'http://itaigi.tw/k/kkk?%25E6%25BC%25A2%25E5%25AD%2597=AA',
                '%25E9%259F%25B3%25E6%25A8%2599': 'BB'
            }
        )
        self.assertEqual(
            回應.url,
            'http://itaigi.tw/k/kkk?' +
            '%25E6%25BC%25A2%25E5%25AD%2597=AA&' +
            '%25E9%259F%25B3%25E6%25A8%2599=BB'
        )
