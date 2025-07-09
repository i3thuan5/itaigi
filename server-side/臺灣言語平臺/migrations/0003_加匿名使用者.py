# -*- coding: utf-8 -*-
from django.db import migrations


def _加匿名者(apps, schema_editor):
    來源表 = apps.get_model("臺灣言語資料庫", "來源表")
    來源 = 來源表.objects.get_or_create(名='匿名')[0]

    使用者表 = apps.get_model("臺灣言語平臺", "使用者表")
    使用者表.objects.create(來源=來源, email='nobody@g0v.tw')


class Migration(migrations.Migration):

    dependencies = [
        ('臺灣言語平臺', '0002_正規化sheet表'),
    ]

    operations = [
        migrations.RunPython(_加匿名者),
    ]
