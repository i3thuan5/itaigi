from datetime import datetime
import io
from os.path import dirname, join
from urllib import request

import yaml


from 臺灣言語資料庫.資料模型 import 文本表
from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語資料庫.資料模型 import 版權表
from 臺灣言語資料庫.資料模型 import 外語表
from 臺灣言語資料庫.資料模型 import 影音表
from 臺灣言語資料庫.資料模型 import 資料表工具


class 匯出入工具:

    def __init__(self, 收錄者=None):
        if 收錄者:
            self.收錄者 = 收錄者
        else:
            self.收錄者 = 來源表.objects.get_or_create(名='系統管理者')[0]

    @classmethod
    def 顯示資料狀態(cls):
        return '{}。這馬時間：{}'.format(
            資料表工具.顯示資料數量(),
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )

    def 匯入檔案(self, 檔名, 匯入影音=True):
        with io.open(檔名) as 檔案:
            self._匯入物件(檔案, dirname(檔名), 匯入影音)

    def 匯入網址(self, 網址, 匯入影音=True):
        with request.urlopen(網址) as 檔案:
            self._匯入物件(檔案, None, 匯入影音)

    def _匯入物件(self, yaml檔案資料, 資料目錄, 匯入影音):
        資料物件 = yaml.load(yaml檔案資料)
        版權表.objects.get_or_create(版權=資料物件['版權'])
        self._遞迴匯入物件(
            資料物件,
            {'收錄者': self.收錄者},
            None,
            資料目錄,
            匯入影音
        )

    def _遞迴匯入物件(self, 資料物件, 原本狀態, 頂懸層語料, 資料目錄, 匯入影音):
        這馬狀態 = {}
        這馬狀態.update(原本狀態)
        下層物件陣列 = None
        for 欄位, 內容 in 資料物件.items():
            if 欄位 == '下層':
                下層物件陣列 = 內容
            else:
                這馬狀態[欄位] = 內容
        這層語料 = self._加入資料庫(這馬狀態, 頂懸層語料, 資料目錄, 匯入影音)
        下層公家狀態 = self._清掉狀態資料(這馬狀態)
        if 下層物件陣列:
            for 下層物件 in 下層物件陣列:
                if '相關資料組' in 下層物件:
                    self._匯入相關資料陣列(下層物件['相關資料組'], 下層公家狀態, 這層語料, 資料目錄, 匯入影音)
                else:
                    self._遞迴匯入物件(下層物件, 下層公家狀態, 這層語料, 資料目錄, 匯入影音)

    def _匯入相關資料陣列(self, 相關資料陣列, 原本狀態, 頂懸層語料, 資料目錄, 匯入影音):
        for 相關資料 in 相關資料陣列:
            這馬狀態 = {}
            這馬狀態.update(原本狀態)
            這馬狀態.update(相關資料)
            頂懸層語料 = self._加入資料庫(這馬狀態, 頂懸層語料, 資料目錄, 匯入影音)

    def _清掉狀態資料(self, 這馬狀態):
        新狀態 = {}
        新狀態.update(這馬狀態)
        for 欄位 in ['外語資料', '外語語言', '影音所在', '文本資料']:
            try:
                新狀態.pop(欄位)
            except KeyError:
                pass
        return 新狀態

    def _加入資料庫(self, 這馬狀態, 頂懸層語料, 資料目錄, 匯入影音):
        if '外語資料' in 這馬狀態:
            if 頂懸層語料 is None:
                return 外語表.加資料(這馬狀態)
            raise RuntimeError(
                '型態有問題！！外語袂使有頂懸層語料，頂懸層型態：{}'.format(頂懸層語料.__class__.__name__))
        elif '影音所在' in 這馬狀態:
            if 匯入影音:
                這馬狀態['影音所在'] = join(資料目錄, 這馬狀態['影音所在'])
                if 頂懸層語料 is None:
                    return 影音表.加資料(這馬狀態)
                return 頂懸層語料.錄母語(這馬狀態)
        elif '文本資料' in 這馬狀態:
            if 頂懸層語料 is None:
                return 文本表.加資料(這馬狀態)
            if 頂懸層語料.__class__ == 外語表:
                return 頂懸層語料.翻母語(這馬狀態)
            if 頂懸層語料.__class__ == 影音表:
                return 頂懸層語料.寫文本(這馬狀態)
#             if 頂懸層語料.__class__ == 文本表:
            return 頂懸層語料.校對做(這馬狀態)
        return 頂懸層語料
