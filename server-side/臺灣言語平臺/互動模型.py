# from django.db import models
#
#
# from 臺灣言語資料庫.資料模型 import 來源表
# from 臺灣言語平臺.項目模型 import 平臺項目表
# from 臺灣言語資料庫.資料模型 import 資料類型表
#
# class 評分狀況表(models.Model):
#     使用者 = models.ForeignKey(來源表, related_name='+')
#     項目 = models.ForeignKey(平臺項目表, related_name='+')
#     分數 = models.IntegerField()
#
# class 評分總合表(models.Model):
#     '敢有需要這個表？'
#     項目 = models.OneToOneField(平臺項目表, related_name='評分總合表')
#     正規化結果 = models.BooleanField(default=False)
#     分數 = models.IntegerField()
#
# class 意見表(models.Model):
#     使用者 = models.ForeignKey(來源表, related_name='+')
#     項目 = models.ForeignKey(平臺項目表, related_name='意見')
#     發表時間 = models.DateTimeField(auto_now_add=True)
#     內容 = models.TextField()
#
# class 代誌列表(models.Model):
# #     產生資料、意見、評分、…
#     代誌名 = models.CharField(unique=True, max_length=20)
#
# class 做代誌的分數表(models.Model):
#     資料類型 = models.ForeignKey(資料類型表, related_name='+')
#     代誌 = models.ForeignKey(代誌列表, related_name='+')
#     上少分數 = models.IntegerField()
#     做了分數變化 = models.IntegerField()
#
# class 項目解釋表(models.Model):
#     使用者 = models.ForeignKey(平臺項目表, unique=True, related_name='+')
#     原始鸔釋資料 = models.FileField()
#     網頁鸔釋資料 = models.FileField()
#     class Meta:
#         abstract = True
#
# class 解釋圖表(項目解釋表):
#     圖 = models.ForeignKey(平臺項目表, related_name='解釋圖')
#
# class 解釋聲表(項目解釋表):
#     聲 = models.ForeignKey(平臺項目表, related_name='解釋聲')
#
# class 解釋影音表(項目解釋表):
#     影音 = models.ForeignKey(平臺項目表, related_name='解釋影音')
