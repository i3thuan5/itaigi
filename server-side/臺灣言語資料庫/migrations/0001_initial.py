# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.db.models.deletion import CASCADE
import 臺灣言語資料庫.資料模型


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='來源屬性表',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('分類', models.CharField(max_length=20)),
                ('性質', models.TextField()),
            ],
            bases=(models.Model, 臺灣言語資料庫.資料模型.屬性表函式),
        ),
        migrations.CreateModel(
            name='來源表',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('名', models.CharField(max_length=100)),
                ('屬性', models.ManyToManyField(to='臺灣言語資料庫.來源屬性表')),
            ],
        ),
        migrations.CreateModel(
            name='外語表',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('收錄時間', models.DateTimeField(auto_now_add=True)),
                ('外語資料', models.TextField()),
                ('來源', models.ForeignKey(related_name='+', to='臺灣言語資料庫.來源表', on_delete=CASCADE)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='影音文本表',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='影音聽拍表',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='影音表',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('收錄時間', models.DateTimeField(auto_now_add=True)),
                ('原始影音資料', models.FileField(blank=True, upload_to='')),
                ('網頁影音資料', models.FileField(blank=True, upload_to='')),
                ('來源', models.ForeignKey(related_name='+', to='臺灣言語資料庫.來源表', on_delete=CASCADE)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='文本校對表',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='文本表',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('收錄時間', models.DateTimeField(auto_now_add=True)),
                ('文本資料', models.TextField()),
                ('來源', models.ForeignKey(related_name='+', to='臺灣言語資料庫.來源表', on_delete=CASCADE)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='版權表',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('版權', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='種類表',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('種類', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='翻譯影音表',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('外語', models.ForeignKey(related_name='翻譯影音', to='臺灣言語資料庫.外語表', on_delete=CASCADE)),
                ('影音', models.OneToOneField(related_name='來源外語', to='臺灣言語資料庫.影音表', on_delete=CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='翻譯文本表',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('外語', models.ForeignKey(related_name='翻譯文本', to='臺灣言語資料庫.外語表', on_delete=CASCADE)),
                ('文本', models.OneToOneField(related_name='來源外語', to='臺灣言語資料庫.文本表', on_delete=CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='聽拍校對表',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='聽拍表',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('收錄時間', models.DateTimeField(auto_now_add=True)),
                ('聽拍資料', models.TextField()),
                ('來源', models.ForeignKey(related_name='+', to='臺灣言語資料庫.來源表', on_delete=CASCADE)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='聽拍規範表',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('規範名', models.CharField(max_length=20, unique=True)),
                ('範例', models.TextField()),
                ('說明', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='著作年表',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('著作年', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='著作所在地表',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('著作所在地', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='語言腔口表',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('語言腔口', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='資料屬性表',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('分類', models.CharField(db_index=True, max_length=20)),
                ('性質', models.TextField()),
            ],
            bases=(models.Model, 臺灣言語資料庫.資料模型.屬性表函式),
        ),
        migrations.CreateModel(
            name='資料類型表',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('類型', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='資料屬性表',
            unique_together=set([('分類', '性質')]),
        ),
        migrations.AddField(
            model_name='聽拍表',
            name='屬性',
            field=models.ManyToManyField(to='臺灣言語資料庫.資料屬性表'),
        ),
        migrations.AddField(
            model_name='聽拍表',
            name='收錄者',
            field=models.ForeignKey(related_name='+', to='臺灣言語資料庫.來源表', on_delete=CASCADE),
        ),
        migrations.AddField(
            model_name='聽拍表',
            name='版權',
            field=models.ForeignKey(related_name='+', to='臺灣言語資料庫.版權表', on_delete=CASCADE),
        ),
        migrations.AddField(
            model_name='聽拍表',
            name='種類',
            field=models.ForeignKey(related_name='+', to='臺灣言語資料庫.種類表', on_delete=CASCADE),
        ),
        migrations.AddField(
            model_name='聽拍表',
            name='著作年',
            field=models.ForeignKey(related_name='+', to='臺灣言語資料庫.著作年表', on_delete=CASCADE),
        ),
        migrations.AddField(
            model_name='聽拍表',
            name='著作所在地',
            field=models.ForeignKey(related_name='+', to='臺灣言語資料庫.著作所在地表', on_delete=CASCADE),
        ),
        migrations.AddField(
            model_name='聽拍表',
            name='規範',
            field=models.ForeignKey(related_name='全部資料', to='臺灣言語資料庫.聽拍規範表', on_delete=CASCADE),
        ),
        migrations.AddField(
            model_name='聽拍表',
            name='語言腔口',
            field=models.ForeignKey(related_name='+', to='臺灣言語資料庫.語言腔口表', on_delete=CASCADE),
        ),
        migrations.AddField(
            model_name='聽拍校對表',
            name='新聽拍',
            field=models.OneToOneField(related_name='來源校對資料', to='臺灣言語資料庫.聽拍表', on_delete=CASCADE),
        ),
        migrations.AddField(
            model_name='聽拍校對表',
            name='舊聽拍',
            field=models.ForeignKey(related_name='聽拍校對', to='臺灣言語資料庫.聽拍表', on_delete=CASCADE),
        ),
        migrations.AddField(
            model_name='文本表',
            name='屬性',
            field=models.ManyToManyField(to='臺灣言語資料庫.資料屬性表'),
        ),
        migrations.AddField(
            model_name='文本表',
            name='收錄者',
            field=models.ForeignKey(related_name='+', to='臺灣言語資料庫.來源表', on_delete=CASCADE),
        ),
        migrations.AddField(
            model_name='文本表',
            name='版權',
            field=models.ForeignKey(related_name='+', to='臺灣言語資料庫.版權表', on_delete=CASCADE),
        ),
        migrations.AddField(
            model_name='文本表',
            name='種類',
            field=models.ForeignKey(related_name='+', to='臺灣言語資料庫.種類表', on_delete=CASCADE),
        ),
        migrations.AddField(
            model_name='文本表',
            name='著作年',
            field=models.ForeignKey(related_name='+', to='臺灣言語資料庫.著作年表', on_delete=CASCADE),
        ),
        migrations.AddField(
            model_name='文本表',
            name='著作所在地',
            field=models.ForeignKey(related_name='+', to='臺灣言語資料庫.著作所在地表', on_delete=CASCADE),
        ),
        migrations.AddField(
            model_name='文本表',
            name='語言腔口',
            field=models.ForeignKey(related_name='+', to='臺灣言語資料庫.語言腔口表', on_delete=CASCADE),
        ),
        migrations.AddField(
            model_name='文本校對表',
            name='新文本',
            field=models.OneToOneField(related_name='來源校對資料', to='臺灣言語資料庫.文本表', on_delete=CASCADE),
        ),
        migrations.AddField(
            model_name='文本校對表',
            name='舊文本',
            field=models.ForeignKey(related_name='文本校對', to='臺灣言語資料庫.文本表', on_delete=CASCADE),
        ),
        migrations.AddField(
            model_name='影音表',
            name='屬性',
            field=models.ManyToManyField(to='臺灣言語資料庫.資料屬性表'),
        ),
        migrations.AddField(
            model_name='影音表',
            name='收錄者',
            field=models.ForeignKey(related_name='+', to='臺灣言語資料庫.來源表', on_delete=CASCADE),
        ),
        migrations.AddField(
            model_name='影音表',
            name='版權',
            field=models.ForeignKey(related_name='+', to='臺灣言語資料庫.版權表', on_delete=CASCADE),
        ),
        migrations.AddField(
            model_name='影音表',
            name='種類',
            field=models.ForeignKey(related_name='+', to='臺灣言語資料庫.種類表', on_delete=CASCADE),
        ),
        migrations.AddField(
            model_name='影音表',
            name='著作年',
            field=models.ForeignKey(related_name='+', to='臺灣言語資料庫.著作年表', on_delete=CASCADE),
        ),
        migrations.AddField(
            model_name='影音表',
            name='著作所在地',
            field=models.ForeignKey(related_name='+', to='臺灣言語資料庫.著作所在地表', on_delete=CASCADE),
        ),
        migrations.AddField(
            model_name='影音表',
            name='語言腔口',
            field=models.ForeignKey(related_name='+', to='臺灣言語資料庫.語言腔口表', on_delete=CASCADE),
        ),
        migrations.AddField(
            model_name='影音聽拍表',
            name='影音',
            field=models.ForeignKey(related_name='影音聽拍', to='臺灣言語資料庫.影音表', on_delete=CASCADE),
        ),
        migrations.AddField(
            model_name='影音聽拍表',
            name='聽拍',
            field=models.OneToOneField(related_name='+', to='臺灣言語資料庫.聽拍表', on_delete=CASCADE),
        ),
        migrations.AddField(
            model_name='影音文本表',
            name='影音',
            field=models.ForeignKey(related_name='影音文本', to='臺灣言語資料庫.影音表', on_delete=CASCADE),
        ),
        migrations.AddField(
            model_name='影音文本表',
            name='文本',
            field=models.OneToOneField(related_name='來源影音', to='臺灣言語資料庫.文本表', on_delete=CASCADE),
        ),
        migrations.AddField(
            model_name='外語表',
            name='外語語言',
            field=models.ForeignKey(related_name='+', to='臺灣言語資料庫.語言腔口表', on_delete=CASCADE),
        ),
        migrations.AddField(
            model_name='外語表',
            name='屬性',
            field=models.ManyToManyField(to='臺灣言語資料庫.資料屬性表'),
        ),
        migrations.AddField(
            model_name='外語表',
            name='收錄者',
            field=models.ForeignKey(related_name='+', to='臺灣言語資料庫.來源表', on_delete=CASCADE),
        ),
        migrations.AddField(
            model_name='外語表',
            name='版權',
            field=models.ForeignKey(related_name='+', to='臺灣言語資料庫.版權表', on_delete=CASCADE),
        ),
        migrations.AddField(
            model_name='外語表',
            name='種類',
            field=models.ForeignKey(related_name='+', to='臺灣言語資料庫.種類表', on_delete=CASCADE),
        ),
        migrations.AddField(
            model_name='外語表',
            name='著作年',
            field=models.ForeignKey(related_name='+', to='臺灣言語資料庫.著作年表', on_delete=CASCADE),
        ),
        migrations.AddField(
            model_name='外語表',
            name='著作所在地',
            field=models.ForeignKey(related_name='+', to='臺灣言語資料庫.著作所在地表', on_delete=CASCADE),
        ),
        migrations.AddField(
            model_name='外語表',
            name='語言腔口',
            field=models.ForeignKey(related_name='+', to='臺灣言語資料庫.語言腔口表', on_delete=CASCADE),
        ),
        migrations.AlterUniqueTogether(
            name='來源屬性表',
            unique_together=set([('分類', '性質')]),
        ),
    ]
