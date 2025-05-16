# -*- coding: utf-8 -*-
from django.db import migrations
from 臺灣言語資料庫.欄位資訊 import 字詞
from 臺灣言語資料庫.欄位資訊 import 語句


def _種類加字詞佮語句(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    種類表 = apps.get_model("臺灣言語資料庫", "種類表")
    種類表.objects.get_or_create(種類=語句)
    種類表.objects.get_or_create(種類=字詞)


class Migration(migrations.Migration):

    dependencies = [
        ('臺灣言語資料庫', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(_種類加字詞佮語句),
    ]
