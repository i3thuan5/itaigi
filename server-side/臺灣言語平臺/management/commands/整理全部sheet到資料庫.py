from django.core.management.base import BaseCommand


from 臺灣言語平臺.正規化團隊模型 import 正規化sheet表


class Command(BaseCommand):
    help = '整理全部sheet到資料庫'

    def handle(self, *args, **參數):
        正規化sheet表.全部整理到資料庫()
