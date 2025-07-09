# -*- coding: utf-8 -*-
from django.conf.urls import url


from 臺灣言語平臺.介面.csrf import 看csrf
from 臺灣言語平臺.介面.加資料 import 加外語請教條
from 臺灣言語平臺.介面.加資料 import 加新詞影音
from 臺灣言語平臺.介面.加資料 import 外語加新詞文本
from 臺灣言語平臺.介面.改資料 import 把測試資料藏起來
from 臺灣言語平臺.介面.改資料 import 把測試資料藏起來_管理目錄
from 臺灣言語平臺.介面.揣外語請教條 import 揣外語請教條
from 臺灣言語平臺.介面.看資料內容 import 看資料詳細內容
from 臺灣言語平臺.介面.看資料內容 import 看來源內容
from 臺灣言語平臺.介面.看資料內容 import 投票
from 臺灣言語平臺.介面.登出入 import 登入狀況
from 臺灣言語平臺.介面.fb登入sdk import FB登入SDK
from 臺灣言語平臺.介面.前端工具 import 重導向前端
from 臺灣言語平臺.介面.揣外語請教條 import 揣無建議的外語
from 臺灣言語平臺.介面.揣外語請教條 import 揣按呢講外語請教條
from 臺灣言語平臺.介面.工作 import 正規化表馬上匯入資料庫
from 臺灣言語平臺.介面.貢獻者 import 貢獻者表
from 臺灣言語平臺.介面.揣外語請教條 import 揣上新貢獻的外語請教條
from 臺灣言語平臺.介面.貢獻者 import 正規化團隊表
from 臺灣言語平臺.admin import admin_site
from 臺灣言語平臺.介面.匯出資料 import 匯出辭典資料

urlpatterns = [
    url(r'^平臺項目列表/揣列表$', 揣外語請教條),
    url(r'^平臺項目列表/揣無建議的外語', 揣無建議的外語),
    url(r'^平臺項目列表/揣按呢講列表', 揣按呢講外語請教條),
    url(r'^平臺項目列表/揣上新貢獻的外語', 揣上新貢獻的外語請教條),

    url(r'^平臺項目/看詳細內容$', 看資料詳細內容,),
    url(r'^平臺項目來源/看內容$', 看來源內容),
    url(r'^平臺項目/投票$', 投票,),

    url(r'^csrf/看$', 看csrf),
    url(r'^FB登入SDK$', FB登入SDK.as_view()),
    url(r'^導向$', 重導向前端),
    url(r'^貢獻者表$', 貢獻者表),
    url(r'^正規化團隊表$', 正規化團隊表),

    url(r'^使用者/看編號$', 登入狀況),

    url(r'^平臺項目/加外語$', 加外語請教條),
    url(r'^平臺項目/加新詞影音$', 加新詞影音),
    url(r'^平臺項目/加新詞文本$', 外語加新詞文本),

    url(r'^平臺項目/把測試資料藏起來$', 把測試資料藏起來),

    url(r'^管理/隱藏項目$', 把測試資料藏起來_管理目錄),

    url(r'^工作/正規化表馬上匯入資料庫$', 正規化表馬上匯入資料庫),

    url(r'^匯出資料$', 匯出辭典資料),

    url(r'^kuan2li2/', admin_site.urls),
]
