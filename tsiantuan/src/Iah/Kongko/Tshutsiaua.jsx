import React from 'react';
import { Link } from 'react-router';
import './Tshutsiaua.css';
import preview1 from './1.png'
import badge from './app_store_badge.svg'


export default class Tshutsiaua extends React.Component {

  render() {
    return (
    <div className='main ui text container'>
      <div className='kongko' style={{fontSize: "1.2rem", paddingTop: "20px", paddingBottom:"20px"}}>
        <h1>「厝鳥仔講台語」跟讀練習APP上架啦！🎉🎉🎉</h1>
        <p>
          「厝鳥仔講台語」是iTaigi維護團隊意傳科技全新推出台語口說練習App！讓你隨時隨地輕鬆開口講台語，讓口說更輪轉！
        </p>

        <p>
          <img className='preview' src={preview1} alt="主題模式使用範例圖，有例句和評分結果"/>
        </p>

        <section style={{marginBottom:"20px"}}>
          <p>
            🐦‍⬛ 早鳥一年方案超值價！$1,270！(原價 $1,590)🌾🌾🌾
          </p>
          <ul>
            <li>優惠期間：04/25 - 05/25 (一個月時間，千萬別錯過！)</li>
            <li>第一年就享有超低優惠價，讓你划算學透透！</li>
            <li>明年續訂將恢復原價，現在訂最划算！</li>
            <li>📱 無論你是台語新手，還是想練就更道地的氣口，「厝鳥仔講台語」是你最好的選擇！</li>
          </ul>
          <p>
            ✅ 真人發音，自然又親切！<br/>
            ✅ 超過 40 種生活情境主題，實用又有趣！<br/>
            ✅ 獨家語音辨識，隨時知道哪裡要加強！<br/>
            ✅ 挑戰模式，一關一關練，成就感滿滿！<br/>
          </p>
          <p>
            🎁 還在等什麼？趕緊手刀下載「厝鳥仔講台語」，和厝鳥仔一起快樂學台語！
          </p>
          <p>
            🔗 iOS 版 App Store 搜尋：「厝鳥仔講台語」
          </p>
          <p style={{display: "flex", alignItems: "center"}}>
            <span style={{fontSize: "2rem", lineHeight: "3rem"}}>點我下載👉</span>
            <Link target='_blank' to='https://apps.apple.com/app/apple-store/id6743581200?pt=123902979&ct=itaigi&mt=8'>
              <img alt="App Store 下載" width="160px" src={badge} />
            </Link>
          </p>
        </section>

        <section style={{marginBottom:"20px"}}>
          <p>
            📣 貼心提醒：
          </p>
          <ul>
            <li>Android 版本也正在努力開發中，請安卓的朋友們敬請期待！</li>
            <li>本 App 的語音辨識功能目前尚未辨識聲調，主要針對發音的準確度進行判斷喔！</li>
            <li>為注重使用者隱私，本 App不會收集使用者音檔作為任何用途，請安心使用！</li>
            <li>期待已久的白話字版本也正在趕工中，請大家再等等一下！</li>
          </ul>
        </section>

        <hr/>

        <aside style={{marginBottom:"20px"}}>
          <p>
            iTaigi為什麼會想刊廣告呢？
          </p>
          <p>
            考慮iTaigi有客服、主機、資安、人事等等營運成本，另一方面也希望未來有經費可以支持iTaigi改版。因為iTaigi現今還找不到兼顧公益性和財務可行的方案，決定先用台語相關產品做廣告，讓廣告效益能支持iTaigi繼續營運。💪
          </p>
        </aside>
      </div>
    </div>
    );
  }
}
