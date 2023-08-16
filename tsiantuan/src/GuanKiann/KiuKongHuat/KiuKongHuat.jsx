import React from 'react';
import { Promise } from 'bluebird';
var superagent = require('superagent-promise')(require('superagent'), Promise);
import debug from 'debug';
import SangTshut from './SangTshut';
import 後端 from '../../後端';

export default class KiuKongHuat extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      modalIsOpen: false,
    };
  }

  問外語(evt) {
    var 外語內容 = {
      '外語資料': this.props.華語關鍵字,
    };
    superagent.post(後端.加外語())
      .withCredentials()
      .set('Content-Type', 'application/x-www-form-urlencoded')
      .set('X-CSRFToken', this.props.csrftoken)
      .send(外語內容)
      .then(({ body }) => (this.openModal()))
      .catch(res => {
        console.log(res);
      });
  }

  openModal() {
    this.setState({ modalIsOpen: true });
  }

  closeModal() {
    this.setState({ modalIsOpen: false });
  }

  tsusun_kaisiau() {
    window.open(
      'https://calendly.com/itaigi/30min'
    );
  }
  render() {
    let { 華語關鍵字 } = this.props;
    return (
      <div>
        <h2 className='ui header'>
          <i className='child icon'></i>
          知道更多講法
        </h2>
        如果還想知道「{this.props.華語關鍵字}」的講法，你可以：
        <h3>
          <i className='bullhorn icon'></i>
          註冊並公開發問
        </h3>
        <p>
          <i className="sign in  icon"></i>為什麼要註冊？<br/>
          為了讓iTaigi不被廣告、機器人打擾，需要大家註冊再使用。
        </p>
        <button
          className="ui green button"
          onClick={this.問外語.bind(this)}
        >
          註冊並公開發問
        </button>

              <h3>
                <i className='comments icon'></i>
                1對1台語諮詢
              </h3>
              <p>
                如果還想知道「{this.props.華語關鍵字}」其他補充資料，iTaigi提供1對1台語諮詢服務，可以問像是工作上的應答、生活情況、文字翻譯……，30分鐘不限主題讓你問到飽！
              </p>
              <span style={{"marginRight": "20px"}}><b>NT$1,000 / 30分鐘</b></span>
                <div
                  className="ui primary button"
                  onClick={this.tsusun_kaisiau.bind(this)}
                >
                  預約諮詢
              </div>
        <SangTshut modalIsOpen={this.state.modalIsOpen}
          closeModal={this.closeModal.bind(this)}/>
      </div>
      );
  }
}

KiuKongHuat.propTypes = {
  華語關鍵字: React.PropTypes.string,
  csrftoken: React.PropTypes.string,
};
