from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語資料庫.資料模型 import 版權表
from 臺灣言語資料庫.欄位資訊 import 會使公開
from 臺灣言語資料庫.資料模型 import 種類表
from 臺灣言語資料庫.欄位資訊 import 字詞


def before_scenario(context, scenario):
    種類表.objects.get_or_create(種類=字詞)
    來源表.objects.get_or_create(名='匿名')
    版權表.objects.get_or_create(版權=會使公開)


def after_scenario(context, scenario):
    pass
