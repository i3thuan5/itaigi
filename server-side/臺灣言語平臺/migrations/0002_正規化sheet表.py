# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('臺灣言語資料庫', '0003_auto_20151009_0731_版權加長度'),
        ('臺灣言語平臺', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='正規化sheet表',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('client_email', models.CharField(max_length=200)),
                ('private_key', models.CharField(max_length=4000)),
                ('url', models.CharField(max_length=200, unique=True)),
                ('語言腔口', models.OneToOneField(to='臺灣言語資料庫.語言腔口表', related_name='正規化sheet', on_delete=models.CASCADE)),
            ],
        ),
    ]
