import json

from django.core.management.base import BaseCommand


from 臺灣言語平臺.正規化團隊模型 import 正規化sheet表
from django.conf import settings


class Command(BaseCommand):
    help = '加sheet的json'

    def add_arguments(self, parser):
        parser.add_argument(
            '服務帳戶json',
            type=str,
            help='google developers console下載的服務帳戶json'
        )
        parser.add_argument(
            '網址',
            type=str,
            help='google sheet的網址'
        )

    def handle(self, *args, **參數):
        with open(參數['服務帳戶json']) as 檔案:
            服務帳戶資料 = json.load(檔案)
        正規化sheet表.加sheet(
            語言腔口=settings.MOTHER_TONGUE,
            key_file_name=參數['服務帳戶json'],
            url=參數['網址'],
        )
        self.stdout.write(
            '愛記得到「Google Sheets右上角的Share」裡分享「Can edit」的權限予 {} 喲！！'.format(
                服務帳戶資料['client_email']
            )
        )
