# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('臺灣言語資料庫', '0002_加字詞、語句種類'),
    ]

    operations = [
        migrations.AlterField(
            model_name='版權表',
            name='版權',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
