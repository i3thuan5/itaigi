# -*- coding: utf-8 -*-
import json
from unittest.case import skip

from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TestCase


class 文本表加音標資料欄位試驗(TestCase):
    app名 = '臺灣言語資料庫'
    原本migration = [(app名, '0003_auto_20151009_0731_版權加長度')]
    新migration = [(app名, '0004_文本表_音標資料')]

    def setUp(self):
        self.executor = MigrationExecutor(connection)
        self.executor.migrate(self.原本migration)
        self.executor.loader.build_graph()
        self.原本apps = self.executor.loader.project_state(self.原本migration).apps

    def 徙資料庫(self):
        self.executor.loader.build_graph()
        self.executor.migrate(self.新migration)
        self.新apps = self.executor.loader.project_state(self.新migration).apps
        self.新apps.get_model(self.app名, '文本表').objects.get(文本資料='媠')

    @skip('升django2.0就出問題')
    def test_原本屬性有音標(self):
        原本 = self.加文本()
        原本.屬性.add(self.原本apps.get_model(self.app名, '資料屬性表').objects.create(
            分類='音標', 性質=json.dumps('sui2')
        ))

        self.徙資料庫()

        新文本表 = self.新apps.get_model(self.app名, '文本表')
        文本 = 新文本表.objects.get(文本資料='媠')
        self.assertEqual(文本.音標資料, 'sui2')

    @skip('升django2.0就出問題')
    def test_屬性的音標會無去(self):
        原本 = self.加文本()
        原本.屬性.add(self.原本apps.get_model(self.app名, '資料屬性表').objects.create(
            分類='音標', 性質=json.dumps('sui2')
        ))

        self.徙資料庫()

        新文本表 = self.新apps.get_model(self.app名, '文本表')
        文本 = 新文本表.objects.get(文本資料='媠')
        self.assertEqual(文本.屬性.count(), 0)

    def test_原本屬性無音標(self):
        self.加文本()

        self.徙資料庫()

        新文本表 = self.新apps.get_model(self.app名, '文本表')
        文本 = 新文本表.objects.get(文本資料='媠')
        self.assertEqual(文本.音標資料, '')

    def 加文本(self):
        原本文本表 = self.原本apps.get_model(self.app名, '文本表')
        self.Pigu = self.原本apps.get_model(self.app名, '來源表').objects.create(
            名='Dr. Pigu'
        )
        return 原本文本表.objects.create(
            收錄者=self.Pigu,
            來源=self.Pigu,
            版權=self.原本apps.get_model(self.app名, '版權表').objects.create(版權='公開'),
            種類=self.原本apps.get_model(self.app名, '種類表').objects.get(種類='字詞'),
            語言腔口=self.原本apps.get_model(self.app名, '語言腔口表').objects.create(
                語言腔口='333'
            ),
            著作所在地=self.原本apps.get_model(self.app名, '著作所在地表').objects.create(
                著作所在地='konn5'
            ),
            著作年=self.原本apps.get_model(self.app名, '著作年表').objects.create(
                著作年='3'
            ),
            文本資料='媠',
        )
