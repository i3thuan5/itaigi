Feature: 求講法→我來講，要等維護團隊處理後，整個狀態才改變

    Scenario: 一開始攏無人求講法，無建議
       Then 無建議的詞內底無物件
       
    Scenario: 一開始，無講法
       When 有人求 豬 的講法
       Then 查 豬 無任何講法
       
    Scenario: 有人問問題，就有無建議的詞
       When 有人求 豬 的講法
       Then 無建議的詞內底有 豬

    Scenario: 有人回答
       Given 有人求 豬 的講法
       When 有人答 豬仔 的講法
       Then 無建議的詞內底有 豬

    Scenario: 有人回答了嘛是看袂著
       Given 有人求 豬 的講法
       When 有人答 豬仔 的講法
       Then 查 豬 無任何講法

    Scenario: 有人直接分享伊的講法
       When 有人答 豬仔 的講法
       Then 查 豬 無任何講法

    Scenario: 有人正規化了就當做有講法矣
       Given 有人求 豬 的講法
       And 有人答 豬仔 的講法
       When 有人正規化 豬仔 的講法
       Then 無建議的詞內底無物件

    Scenario: 有人正規化愛顯示講法
       Given 有人求 豬 的講法
       And 有人答 豬仔 的講法
       When 有人正規化 豬仔 的講法
       Then 查 豬 會當揣著 豬仔
