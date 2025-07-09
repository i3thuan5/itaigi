from django.contrib import admin
from 臺灣言語平臺.使用者模型 import 使用者表


class 後臺使用者管理(admin.ModelAdmin):
    # change list
    list_display = ['email', '__str__', 'is_staff', ]
    ordering = ['email', ]
    list_filter = ['is_staff']
    search_fields = ['email', '來源__名', ]
    readonly_fields = ['email']
    fields = ('email', 'is_staff',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class 後臺使用者(使用者表):

    class Meta:
        proxy = True
        verbose_name = "後臺使用者"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.來源.名
