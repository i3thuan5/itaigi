import React from 'react';
import Su from '../Su/Su';
import SuTsitPuann from '../Su/SuTsitPuann';
import ABo from '../../GuanKiann/ABo/ABo';
import Debug from 'debug';
import './GuaGi.css';

var debug = Debug('itaigi:GuaGi');

export default class GuaGi extends React.Component {

  dedupeSu(inSu) {
    var seen = {};
    return inSu.filter((val, id) => {
      var key = val.文本資料 + val.音標資料;
      if (seen[key])
        return false;
      seen[key] = true;
      return true;
    });
  }

  顯示詞(詞) {
    let 來開例句 = this.props.開例句.bind(this, this.props.華語關鍵字, 詞.文本資料, 詞.音標資料);
    return <Su
      suId={詞.新詞文本項目編號}
      suText={詞.文本資料}
      suIm={詞.音標資料}
      貢獻者={詞.貢獻者}
      按呢講好={詞.按呢講好}
      按呢無好={詞.按呢無好}
      按呢講的外語列表 = {詞.按呢講的外語列表}
      key={詞.新詞文本項目編號}
      csrftoken={this.props.csrftoken}
      來開例句={來開例句}
      variables={{ 詞 }}
      renderLoading={this.詞載入中(詞, 來開例句)} />;
  }

  詞載入中(詞, 來開例句) {
    return (
      <SuTsitPuann
        詞={詞}
        來開例句={來開例句}/>
      );
  }
  tsusun_kaisiau() {
    window.open(
      'https://docs.google.com/forms/d/e/1FAIpQLSc4Q5HpkjtcN6hmig6nnwu6YuSwnL8Gy6yS7dImBs2kbS0Hsw/viewform'
    );
  }

  render() {
    if (!this.props.新詞文本) {
      return <div></div>;
    }

    var uniqueSu = this.dedupeSu(this.props.新詞文本);

    var suList = uniqueSu.map(this.顯示詞.bind(this));
    return (
    <div className='guaGi'>
      <div className='ui su vertical segment'>
        <div className='ui stackable cards'>
          {suList}

          <div className='ui su card'>
            <div className='content'>
        <h2 className='ui header'>
          <i className='child icon'></i>
          知道更多講法
        </h2>
        如果還想知道「{this.props.華語關鍵字}」的講法，你可以：
        <h3>
          <i className='bullhorn icon'></i>
          再一次公開發問
        </h3>
        <p>
          <i className="sign in  icon"></i>為什麼要註冊？<br/>
          為了讓iTaigi不被廣告、機器人打擾，需要大家註冊再使用。
        </p>
        <button
          className="ui green button"
          // onClick={this.問外語.bind(this)}
        >
          註冊並再一次公開發問
        </button>

              <h3>
                <i className='comments icon'></i>
                1對1台語諮詢
              </h3>
              <p>
                如果還想知道「{this.props.華語關鍵字}」其他補充資料，iTaigi提供1對1台語諮詢服務，可以問像是工作上的應答、生活情況、文字翻譯……，30分鐘不限主題讓你問到飽！
              </p>
              <div
                className="ui button labeled"
              >
                <a className="ui basic label">
                  NT$1,000 / 30分鐘
                </a>
                <div
                  className="ui green button"
                  onClick={this.tsusun_kaisiau.bind(this)}
                >
                  立即預約諮詢
                </div>
              </div>
            </div>
          </div>

          <div className='ui su card'>
            <div className='content'>
              <h2 className='ui header'>
                <i className='cloud upload icon'></i>
                貢獻講法
              </h2>
              <ABo 華語關鍵字={this.props.華語關鍵字}
               csrftoken={this.props.csrftoken}
               編號={this.props.編號} 漢字={this.props.漢字} 音標={this.props.音標}
               />
            </div>
          </div>

        </div>
      </div>
    </div>
    );
  }
}
