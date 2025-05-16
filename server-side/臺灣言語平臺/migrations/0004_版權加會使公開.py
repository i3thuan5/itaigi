# -*- coding: utf-8 -*-
from django.db import migrations
from 臺灣言語資料庫.欄位資訊 import 會使公開


def _版權加會使公開(apps, schema_editor):
    版權表 = apps.get_model("臺灣言語資料庫", "版權表")
    版權表.objects.get_or_create(版權=會使公開)


class Migration(migrations.Migration):

    dependencies = [
        ('臺灣言語平臺', '0003_加匿名使用者'),
    ]

    operations = [
        migrations.RunPython(_版權加會使公開),
    ]
