from django.contrib import admin
from django.db.models.query_utils import Q
from 臺灣言語平臺.項目模型 import 平臺項目表


class 藏華語(平臺項目表):

    class Meta:
        proxy = True
        verbose_name = "藏華語"
        verbose_name_plural = verbose_name

    def 華語(self):
        return self.外語.外語資料


class 藏華語管理(admin.ModelAdmin):
    # change list
    list_display = ['華語', '愛藏起來', ]
    list_editable = ['愛藏起來', ]
    ordering = ['-id', ]
    list_filter = ['愛藏起來']
    search_fields = ['外語__外語資料', ]

    def has_add_permission(self, request):
        # 薛：只能由程式上傳音檔和語料
        # 薛：任何人都不能從後台新增
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(
            Q(外語__isnull=False)
        )

    class Media:
        css = {
            "all": ("css/admin_gi2_liau7_pio2.css", "css/moedictFont.css")
        }
