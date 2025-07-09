from django.core.management.base import BaseCommand


from 臺灣言語資料庫.資料模型 import 資料表工具


class Command(BaseCommand):
    help = '顯示資料數量'

    def handle(self, *args, **參數):
        self.stdout.write(資料表工具.顯示資料數量())
