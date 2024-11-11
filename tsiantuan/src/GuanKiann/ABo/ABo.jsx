import React from 'react';
import { Link } from 'react-router';
import { Promise } from 'bluebird';
import APui from './APui';
import 後端 from '../../後端';
var superagent = require('superagent-promise')(require('superagent'), Promise);
import debug from 'debug';
var log = debug('itaigi:ABo');

export default class ABo extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      漢字: this.props.漢字 || '',
      音標: this.props.音標 || '',
      modalIsOpen: false,
      送出中: false,
    };
  }

  handle漢字KeyUp(evt) {
    var q = evt.target.value;
    this.setState({ 漢字: q });
  }

  handle音標KeyUp(evt) {
    var q = evt.target.value;
    this.setState({ 音標: q });
  }

  查怎樣講(evt) {
    if (this.state.漢字 !== '' || this.state.音標 !== '') {
      var 外語內容 = {
        '外語資料': this.props.華語關鍵字,
      };
      superagent.post(後端.加外語())
        .withCredentials()
        .set('Content-Type', 'application/x-www-form-urlencoded')
        .set('X-CSRFToken', this.props.csrftoken)
        .send(外語內容)
        .then(({ body }) => (this.加外語新詞文本(body.平臺項目編號)))
        .catch(res => {
          window.open(後端.登入(), '_blank');
        });
      this.setState({
        送出中: true,
      });
    }
  }

  加外語新詞文本(外語項目編號) {
    debug(外語項目編號);
    let 建議新詞文本;
    if (this.state.漢字 !== '') {
      建議新詞文本 = {
        '外語項目編號': 外語項目編號,
        '文本資料': this.state.漢字,
        '音標資料': this.state.音標,
      };
    } else {
      建議新詞文本 = {
        '外語項目編號': 外語項目編號,
        '文本資料': this.state.音標,
      };
    }

    superagent.post(後端.加新詞文本())
      .withCredentials()
      .set('Content-Type', 'application/x-www-form-urlencoded')
      .set('X-CSRFToken', this.props.csrftoken)
      .send(建議新詞文本)
      .then(({ body }) => (this.openModal()))
      .catch((a) => (debug(a)));
  }

  openModal() {
    this.setState({ modalIsOpen: true });
  }

  closeModal() {
    this.setState({
      modalIsOpen: false,
      漢字: '',
      音標: '',
      送出中: false,
    });
  }

  render無登入ê鈕仔() {
    return (
      <div className='ui buttons'>
        <button
          className={ 'ui button large' + (this.state.送出中 ? ' disabled' : '') }
          onClick={this.查怎樣講.bind(this)}>匿名送出</button>
      </div>
    );

    // %E6%BC%A2%E5%AD%97 漢字
    // %E9%9F%B3%E6%A8%99 音標
  }

  render() {
    return (
        <div className='ui form'>
            <div className='field'>
                <label>臺語漢字</label>
                <div className='abo ui input large'>
                <input placeholder='臺語漢字' type='text'
                    value={this.state.漢字}
                    onChange={this.handle漢字KeyUp.bind(this)}/>
                </div>
            </div>
            <div className='field'>
                <label>台羅</label>
                <div className='abo ui input large'>
                <input placeholder='台羅' type='text'
                    value={this.state.音標}
                    onChange={this.handle音標KeyUp.bind(this)}/>
                </div>
            </div>
            <div className='field'>
              <label for="cc">
                  <input type='checkbox' id="cc"/> 
                  &nbsp;我同意內容以
                  <a href="https://creativecommons.org/publicdomain/zero/1.0/" target='blank'>CC0 公眾領域貢獻宣告</a>
                  釋出授權到公眾領域。
              </label>
              <label for="unsu">
                <input type='checkbox' id="unsu"/>
                &nbsp;我已經理解<Link to="/unsu">iTaigi隱私權保護條款。</Link>
              </label>
            </div>
          {this.render無登入ê鈕仔()}

            <APui modalIsOpen={this.state.modalIsOpen}
              closeModal={this.closeModal.bind(this)}/>
        </div>
      );
  }
}

ABo.propTypes = {
  漢字: React.PropTypes.string,
  音標: React.PropTypes.string,
  華語關鍵字: React.PropTypes.string,
  csrftoken: React.PropTypes.string,
};
