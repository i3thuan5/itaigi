from django.urls import reverse


def meta_description(request):
    description = None
    if request.path == reverse('miasenn'):
        description = (
            """輸入姓名漢字，查詢對應的台語羅馬字拼音以及聆聽電腦自動發音。"""
        )
    elif request.path.startswith(reverse('pokam')):
        description = (
            """各種主題的台語詞彙專區。"""
        )
    else:
        description = (
            """透過群眾發問、回答，建立現代台語開源辭典，開放大眾查詢。"""
            """辭典內容屬於台灣創用CC授權0，歡迎非商業與商業利用。本專案構"""
            """想來自g0v零時政府萌典開源辭典。"""
        )
    return {
        'meta_description': description
    }
