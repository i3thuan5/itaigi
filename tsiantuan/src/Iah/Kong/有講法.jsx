import React from 'react';
import ABo from '../../GuanKiann/ABo/ABo';
import GuaGi from '../../GuanKiann/GuaGi/GuaGi';
import 分享鍵 from '../../GuanKiann/分享鍵/分享鍵';
import 留言板 from '../../GuanKiann/留言板/留言板';
import 其他建議 from './其他建議';
import Debug from 'debug';

var debug = Debug('itaigi:Kong有講法');

export default class 有講法 extends React.Component {
  tsusun_kaisiau() {
    window.open(
      'https://calendly.com/itaigi/30min'
    );
  }
  render() {
    return (
    <div className='kongHuat'>
      <div className='tsusun-kaisiau tsusunkaisiau'>
        <span>有任何對於台語的疑難雜症嗎？iTaigi提供1對1台語諮詢服務，30分鐘讓你問到飽！</span>

          <div
            className="ui button labeled"
          >
            <a className="ui basic label">
              NT$1,000 / 30分鐘
            </a>
            <div
              className="ui primary button"
              onClick={this.tsusun_kaisiau.bind(this)}
            >
              <i className="heart icon"></i>
              立即預約諮詢
            </div>
        </div>
      </div>
      {this.props.內容.列表.map((g) => (
        <GuaGi id={g.外語項目編號}
          key={g.外語項目編號} 新詞文本={g.新詞文本}
          csrftoken={this.props.csrftoken}
          編號={this.props.編號} 漢字={this.props.漢字} 音標={this.props.音標}
          華語關鍵字={this.props.華語關鍵字}
          開例句={this.props.開例句.bind(this)}
          />
      ))}
      <其他建議
        內容={this.props.內容}
        華語關鍵字={this.props.華語關鍵字}
        開例句={this.props.開例句.bind(this)}/>
      <h3 className='ui horizontal divider header'>
        <i className='outline comments icon'></i>
        來討論
        「<span className='ui pink header'>{this.props.華語關鍵字}</span>」
      </h3>
      <留言板/>
    </div>
    );
  }
}
