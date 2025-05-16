from 臺灣言語資料庫.資料模型 import 外語表
from 臺灣言語工具.解析整理.解析錯誤 import 解析錯誤
from 臺灣言語資料庫.資料模型 import 文本表
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **參數):
        for 外語 in 外語表.全部外語資料():
            try:
                外語.分詞資料()
            except 解析錯誤:
                self.stdout.write(
                    '{}的「」無法度做分詞'.format(外語.來源.名, 外語.外語資料)
                )
        for 文本 in 文本表.objects.all():
            try:
                文本.分詞資料()
            except 解析錯誤:
                self.stdout.write(
                    '{}的「」無法度做分詞'.format(文本.來源.名, 文本.文本資料)
                )
