# -*- coding: utf-8 -*-
from builtins import isinstance
import io
import json
from os.path import join, abspath
from tempfile import mkdtemp
from urllib import request

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import File
from django.db import models
from django.db.models import Count
from django.db.models.deletion import CASCADE

from libavwrapper.avconv import Input, Output, AVConv
from libavwrapper.codec import AudioCodec, NO_VIDEO


from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語資料庫.欄位資訊 import 語句
from 臺灣言語工具.語音辨識.聲音檔 import 聲音檔
from 臺灣言語工具.基本物件.公用變數 import 分型音符號
from 臺灣言語工具.解析整理.文章粗胚 import 文章粗胚


class 屬性表函式:

    def 內容(self):
        return {self.分類: json.loads(self.性質)}

    @classmethod
    def 加屬性(cls, 分類, 性質):
        return cls.objects.get_or_create(分類=分類, 性質=json.dumps(性質))[0]

    @classmethod
    def 揣屬性(cls, 分類, 性質):
        return cls.objects.get(分類=分類, 性質=json.dumps(性質))

    def __str__(self):
        return '{}:{}'.format(self.分類, json.loads(self.性質))

    class Meta:
        unique_together = (('分類', '性質'))


class 來源屬性表(屬性表函式, models.Model):
    分類 = models.CharField(max_length=20)  # 出世地
    性質 = models.TextField()  # json字串格式。 臺灣、…


class 來源表(models.Model):
    名 = models.CharField(max_length=100)  # 人名、冊名、…
    屬性 = models.ManyToManyField(來源屬性表)  # 出世年、出世地、…

    def 屬性內容(self):
        內容結果 = {}
        for 屬性 in self.屬性.all():
            內容結果[屬性.分類] = json.loads(屬性.性質)
        return 內容結果

    def 編號(self):
        return self.pk

    @classmethod
    def 加來源(cls, 內容):
        名 = 內容['名']
        來源 = cls.objects.create(名=名)
        for 分類, 性質 in 內容.items():
            if 分類 != '名':
                來源.屬性.add(來源屬性表.加屬性(分類, 性質))
        return 來源

    @classmethod
    def 揣來源(cls, 內容):
        名 = 內容['名']
        來源屬性陣列 = []
        for 分類, 性質 in 內容.items():
            if 分類 != '名':
                來源屬性 = 來源屬性表.objects.get(分類=分類, 性質=json.dumps(性質))
                來源屬性陣列.append(來源屬性)
        選擇 = 來源表.objects.filter(名=名).annotate(屬性數量=Count('屬性'))
        for 來源屬性 in 來源屬性陣列:
            選擇 = 選擇.filter(屬性=來源屬性)
        return 選擇.get(屬性數量=len(來源屬性陣列))

    def __str__(self):
        return str(self.編號()) + ' ' + self.名


class 版權表(models.Model):
    # 	會使公開，袂使公開
    版權 = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.版權


class 種類表(models.Model):
    # 	字詞 = '字詞'
    # 	語句 = '語句'
    種類 = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.種類


class 語言腔口表(models.Model):
    # 	閩南語、閩南語永靖腔、客話四縣腔、泰雅seediq…
    語言腔口 = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return self.語言腔口

    @classmethod
    def 揣出有文本的語言腔口(cls):
        return cls.objects.filter(
            pk__in=文本表.objects.all().values_list('語言腔口', flat=True).distinct()
        )

    @classmethod
    def 揣出有語句文本的語言腔口(cls):
        語句種類 = 種類表.objects.get(種類=語句)
        return cls.objects.filter(
            pk__in=文本表.objects.filter(種類=語句種類).values_list(
                '語言腔口', flat=True).distinct()
        )


class 著作所在地表(models.Model):
    # 	臺灣、員林、…
    著作所在地 = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return self.著作所在地


class 著作年表(models.Model):
    # 	1952、19xx、…
    著作年 = models.CharField(unique=True, max_length=20)

    def __str__(self):
        return self.著作年


class 資料屬性表(屬性表函式, models.Model):
    分類 = models.CharField(max_length=20, db_index=True)  # 詞性、語者…
    性質 = models.TextField()  # json字串格式。名詞、…


class 資料表(models.Model):

    class Meta:
        abstract = True
    收錄者 = models.ForeignKey(來源表, related_name='+', on_delete=CASCADE)
    收錄時間 = models.DateTimeField(auto_now_add=True)
    來源 = models.ForeignKey(來源表, related_name='+', on_delete=CASCADE)
    版權 = models.ForeignKey(版權表, related_name='+', on_delete=CASCADE)
    種類 = models.ForeignKey(種類表, related_name='+', on_delete=CASCADE)
    語言腔口 = models.ForeignKey(語言腔口表, related_name='+', on_delete=CASCADE)
    著作所在地 = models.ForeignKey(著作所在地表, related_name='+', on_delete=CASCADE)
    著作年 = models.ForeignKey(著作年表, related_name='+', on_delete=CASCADE)
    屬性 = models.ManyToManyField(資料屬性表)  # 詞性,分類,…

    def 編號(self):
        return self.pk

    def 屬性內容(self):
        內容結果 = {}
        for 屬性 in self.屬性.all():
            內容結果[屬性.分類] = json.loads(屬性.性質)
        return 內容結果

    @classmethod
    def 資料數量(cls):
        return cls.objects.all().count()

    def _加基本內容而且儲存(self, 內容):
        self.收錄者 = self._揣來源資料(內容['收錄者'], False)
        self.來源 = self._揣來源資料(內容['來源'], True)
        for 欄位名 in [
            版權表,
            種類表,
        ]:
            self._設定欄位(內容, 欄位名, False)
        for 欄位名 in [
            語言腔口表,
            著作所在地表,
            著作年表,
        ]:
            self._設定欄位(內容, 欄位名, True)
        self.full_clean()
        try:
            self._設定屬性而且存入資料庫(內容['屬性'])
        except KeyError:
            self.save()

    def _內容轉物件(self, 內容):
        try:
            return json.loads(內容)
        except Exception:
            return 內容

    def _揣來源資料(self, 內容資料, 會使加新的):
        if isinstance(內容資料, int):
            return 來源表.objects.get(pk=內容資料)
        if isinstance(內容資料, str) or isinstance(內容資料, dict):
            來源物件 = self._內容轉物件(內容資料)
            try:
                return 來源表.揣來源(來源物件)
            except TypeError:
                raise ValueError('來源毋是有效字串！！')
            except ObjectDoesNotExist:
                if 會使加新的:
                    return 來源表.加來源(來源物件)
                raise
        return 內容資料

    def _設定欄位(self, 內容, 資料表, 會使加新的):
        欄位名 = 資料表.__name__[:-1]
        內容資料 = 內容[欄位名]
        if isinstance(內容資料, int):
            setattr(self, 欄位名, 資料表.objects.get(pk=內容資料))
        elif isinstance(內容資料, str):
            if 會使加新的:
                setattr(self, 欄位名, 資料表.objects.get_or_create(**{欄位名: 內容資料})[0])
            else:
                setattr(self, 欄位名, 資料表.objects.get(**{欄位名: 內容資料}))
        else:
            setattr(self, 欄位名, 內容資料)

    def _設定屬性而且存入資料庫(self, 屬性內容):
        屬性物件 = self._內容轉物件(屬性內容)
        try:
            屬性物件.items()
        except AttributeError:
            raise ValueError('屬性內容資料愛是辭典型態')
        self.save()
        for 分類, 性質 in 屬性物件.items():
            self.屬性.add(
                資料屬性表.objects.get_or_create(分類=分類, 性質=json.dumps(性質))[0]
            )

    def _加關係的內容檢查(self, 內容):
        if 內容['種類'] != self.種類.種類:
            raise ValueError(
                '新資料的種類「{}」愛佮原本資料的種類「{}」仝款！！'.format(
                    內容['種類'],
                    self.種類.種類
                )
            )
        if 內容['語言腔口'] != self.語言腔口.語言腔口:
            raise ValueError(
                '新資料的語言腔口「{}」愛佮原本資料的語言腔口「{}」仝款！！'.format(
                    內容['語言腔口'],
                    self.語言腔口.語言腔口)
            )


class 外語表(資料表):
    外語語言 = models.ForeignKey(語言腔口表, related_name='+', on_delete=CASCADE)
    外語資料 = models.TextField(blank=False)

    def __str__(self):
        return self.外語資料

    @classmethod
    def 加資料(cls, 輸入內容):
        外語 = cls()
        內容 = 外語._內容轉物件(輸入內容)
        if isinstance(內容['外語語言'], int):
            外語.外語語言 = 語言腔口表.objects.get(pk=內容['外語語言'])
        elif isinstance(內容['外語語言'], str):
            外語.外語語言 = 語言腔口表.objects.get_or_create(語言腔口=內容['外語語言'])[0]
        else:
            外語.外語語言 = 內容['外語語言']
        if isinstance(內容['外語資料'], str):
            外語.外語資料 = 內容['外語資料']
        else:
            raise ValueError('外語資料必須愛是字串型態')
        外語._加基本內容而且儲存(內容)
        return 外語

    def 錄母語(self, 輸入影音內容):
        影音內容 = self._內容轉物件(輸入影音內容)
        self._加關係的內容檢查(影音內容)
        影音 = 影音表.加資料(影音內容)
        self.翻譯影音.create(影音=影音)
        return 影音

    def 翻母語(self, 輸入文本內容):
        文本內容 = self._內容轉物件(輸入文本內容)
        self._加關係的內容檢查(文本內容)
        文本 = 文本表.加資料(文本內容)
        self.翻譯文本.create(文本=文本)
        return 文本

    def 分詞資料(self):
        句物件 = 拆文分析器.建立句物件(文章粗胚.建立物件語句前減號變標點符號(self.外語資料))
        return 句物件.看分詞().replace(分型音符號, '|')

    @classmethod
    def 全部外語資料(cls):
        return cls.objects.all()


class 影音表(資料表):
    影音資料 = models.FileField(blank=True)

    def __str__(self):
        return str(self.影音資料)

    @classmethod
    def 加資料(cls, 輸入內容):
        影音 = cls()
        內容 = 影音._內容轉物件(輸入內容)
        if '影音所在' in 內容 and '影音資料' in 內容:
            raise ValueError('「所在」佮「資料」提供一个就好！！')
        if '影音所在' in 內容 and '影音資料' not in 內容:
            return cls._影音所在加資料(內容)
        if not hasattr(內容['影音資料'], 'read'):
            raise ValueError('影音資料必須是檔案')
        影音._加基本內容而且儲存(內容)
        影音._存影音資料(內容['影音資料'])
        return 影音

    @classmethod
    def _影音所在加資料(cls, 舊內容):
        新內容 = {}
        新內容.update(舊內容)
        所在 = 新內容.pop('影音所在')
        try:
            with io.open(所在, 'rb') as 檔案:
                新內容['影音資料'] = 檔案
                return cls.加資料(新內容)
        except Exception:
            if not 所在.startswith('http://') and not 所在.startswith('https://'):
                所在 = 'http://' + 所在
            with request.urlopen(所在) as 檔案:
                with io.BytesIO(檔案.read()) as 暫存:
                    新內容['影音資料'] = 暫存
                    return cls.加資料(新內容)

    def 寫文本(self, 輸入文本內容):
        文本內容 = self._內容轉物件(輸入文本內容)
        self._加關係的內容檢查(文本內容)
        文本 = 文本表.加資料(文本內容)
        self.影音文本.create(文本=文本)
        return 文本

    def 寫聽拍(self, 輸入聽拍內容):
        聽拍內容 = self._內容轉物件(輸入聽拍內容)
        self._加關係的內容檢查(聽拍內容)
        聽拍 = 聽拍表._加資料(聽拍內容)
        self.影音聽拍.create(聽拍=聽拍)
        return 聽拍

    @classmethod
    def 源頭的影音資料(cls):
        return cls.objects.filter(來源外語=None)

    def 聲音檔(self):
        return 聲音檔.對檔案讀(join(settings.MEDIA_ROOT, self.影音資料.name))

    def 影音所在(self):
        return join(abspath(settings.MEDIA_ROOT), self.影音資料.name)

    def _存影音資料(self, 影音資料):
        self.影音資料.save(
            name='影音資料{0:07}'.format(self.編號()),
            content=File(影音資料),
            save=True
        )
        self.影音資料.close()

    def 網頁聲音資料(self):
        目錄 = mkdtemp()
        所在 = join(目錄, '網頁影音資料.mp3')
        網頁聲音格式 = AudioCodec('libmp3lame')
        網頁聲音格式.channels(1)
        網頁聲音格式.frequence(16000)
        網頁聲音格式.bitrate('128k')
        原始檔案 = Input(self.影音所在())
        網頁檔案 = Output(所在)
        指令 = AVConv('avconv', 原始檔案, 網頁聲音格式, NO_VIDEO, 網頁檔案)
        程序 = 指令.run()
        結果 = 程序.wait()
        if 結果 != 0:
            raise OSError(
                'avconv指令執行失敗，回傳值：{0}\n指令：{1}\n執行訊息：\n{2}'.format(
                    結果, 指令, '\n'.join(程序.readlines())
                )
            )
        with open(所在, 'rb') as 網頁聲音音檔:
            return 網頁聲音音檔.read()


class 文本表(資料表):
    文本資料 = models.TextField(blank=False)
    音標資料 = models.TextField(blank=True)

    def __str__(self):
        try:
            return self.看分詞()
        except Exception:
            return self.文本資料

    @classmethod
    def 加資料(cls, 輸入內容):
        文本 = cls()
        內容 = 文本._內容轉物件(輸入內容)
        try:
            內容['屬性'] = 文本._內容轉物件(內容['屬性'])
        except Exception:
            pass
        if isinstance(內容['文本資料'], str):
            文本.文本資料 = 內容['文本資料']
        else:
            raise ValueError('文本資料必須愛是字串型態')
        文本._揣出內容的音標資料(內容)
        文本._加基本內容而且儲存(內容)
        return 文本

    def _揣出內容的音標資料(self, 內容):
        try:
            self.音標資料 = 內容.pop('音標資料')
            return
        except Exception:
            pass
        try:
            self.音標資料 = 內容['屬性'].pop('音標')
        except Exception:
            self.音標資料 = ''

    def 校對做(self, 輸入文本內容):
        文本內容 = self._內容轉物件(輸入文本內容)
        self._加關係的內容檢查(文本內容)
        文本 = 文本表.加資料(文本內容)
        self.文本校對.create(新文本=文本)
        return 文本

    def 是校對後的資料(self):
        return hasattr(self, '來源校對資料')

    def 分詞資料(self, 拼音=None):
        try:
            對齊句物件 = 拆文分析器.對齊句物件(
                self.文本資料,
                self.音標資料
            )
            return 對齊句物件.看分詞()
        except Exception:
            try:
                拼音.音標上長長度
            except Exception:
                句物件 = 拆文分析器.建立句物件(
                    文章粗胚.建立物件語句前減號變標點符號(
                        self.文本資料
                    )
                )
            else:
                句物件 = 拆文分析器.建立句物件(
                    文章粗胚.建立物件語句前處理減號(
                        拼音,
                        self.文本資料
                    )
                )
            return 句物件.看分詞().replace(分型音符號, '|')

    @classmethod
    def 源頭的文本資料(cls):
        return cls.objects.filter(
            來源外語=None, 來源影音=None, 來源校對資料=None
        )

    @classmethod
    def 上尾層的文本資料(cls):
        return cls.objects.filter(文本校對=None)


class 聽拍表(資料表):
    # 	語者詳細資料記佇屬性內底，逐句話記是佗一个語者
    聽拍資料 = models.TextField()  # 存json.dumps的資料

    def __str__(self):
        try:
            return self.聽拍內容()[0]['內容']
        except Exception:
            return self.聽拍資料

    @classmethod
    def _加資料(cls, 輸入內容):
        聽拍 = cls()
        內容 = 聽拍._內容轉物件(輸入內容)
        聽拍資料內容 = 聽拍._內容轉物件(內容['聽拍資料'])
        try:
            for 一句 in 聽拍資料內容:
                if not isinstance(一句, dict):
                    raise ValueError('聽拍資料內底應該是字典型態')
                if '內容' not in 一句:
                    raise KeyError('逐句聽拍資料攏愛有「內容」欄位')
        except TypeError:
            raise ValueError('聽拍資料應該是字典型態')
        聽拍.聽拍資料 = json.dumps(聽拍資料內容)
        聽拍._加基本內容而且儲存(內容)
        return 聽拍

    def 聽拍內容(self):
        return json.loads(self.聽拍資料)

    def 校對做(self, 輸入聽拍內容):
        聽拍內容 = self._內容轉物件(輸入聽拍內容)
        self._加關係的內容檢查(聽拍內容)
        聽拍 = 聽拍表._加資料(聽拍內容)
        self.聽拍校對.create(新聽拍=聽拍)
        return 聽拍

    def 是校對後的資料(self):
        return hasattr(self, '來源校對資料')


class 資料表工具:

    @classmethod
    def 顯示資料數量(cls):
        return '外語有{}筆，影音有{}筆，文本有{}筆，聽拍有{}筆'.format(
            外語表.資料數量(),
            影音表.資料數量(),
            文本表.資料數量(),
            聽拍表.資料數量(),
        )
