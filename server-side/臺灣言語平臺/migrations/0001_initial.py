# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('臺灣言語資料庫', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='使用者表',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('來源', models.OneToOneField(primary_key=True, serialize=False, to='臺灣言語資料庫.來源表', related_name='使用者', on_delete=models.CASCADE)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('註冊時間', models.DateTimeField(auto_now_add=True)),
                ('分數', models.IntegerField(default=0)),
                ('is_staff', models.BooleanField(default=False)),
                ('維護團隊', models.ManyToManyField(to='臺灣言語資料庫.語言腔口表')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='平臺項目表',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('是資料源頭', models.BooleanField(default=False)),
                ('推薦用字', models.BooleanField(default=False)),
                ('外語', models.OneToOneField(null=True, to='臺灣言語資料庫.外語表', related_name='平臺項目', on_delete=models.CASCADE)),
                ('影音', models.OneToOneField(null=True, to='臺灣言語資料庫.影音表', related_name='平臺項目', on_delete=models.CASCADE)),
                ('文本', models.OneToOneField(null=True, to='臺灣言語資料庫.文本表', related_name='平臺項目', on_delete=models.CASCADE)),
                ('聽拍', models.OneToOneField(null=True, to='臺灣言語資料庫.聽拍表', related_name='平臺項目', on_delete=models.CASCADE)),
            ],
        ),
    ]
