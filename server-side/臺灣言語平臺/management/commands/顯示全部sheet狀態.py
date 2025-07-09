import OpenSSL
from django.core.management.base import BaseCommand
from gspread.exceptions import SpreadsheetNotFound
from oauth2client.client import AccessTokenRefreshError


from 臺灣言語平臺.正規化團隊模型 import 正規化sheet表


class Command(BaseCommand):
    help = '顯示全部sheet狀態，看設定有著無'

    def handle(self, *args, **參數):
        數量 = 0
        for 數量, sheet資料 in enumerate(正規化sheet表.全部資料(), start=1):
            try:
                資料表 = sheet資料.提著資料表()
                if 資料表 is None:
                    raise ValueError('無工作表')
            except AccessTokenRefreshError:
                self.stdout.write(
                    '{}的email有問題'.format(sheet資料.語言腔口.語言腔口)
                )
            except OpenSSL.crypto.Error:
                self.stdout.write(
                    '{}的private_key有問題'.format(sheet資料.語言腔口.語言腔口)
                )
            except SpreadsheetNotFound:
                self.stdout.write(
                    '{}的網址有問題'.format(sheet資料.語言腔口.語言腔口)
                )
            except ValueError:
                self.stdout.write(
                    '{}的sheet內底無工作表'.format(sheet資料.語言腔口.語言腔口)
                )
            else:
                self.stdout.write(
                    '{}設定正常'.format(sheet資料.語言腔口.語言腔口)
                )
        self.stdout.write(
            '攏總有{}个設定'.format(數量)
        )
