import React from 'react';
import { Link } from 'react-router';
import FBTest from '../../FBTest/FBTest';
import 分享鍵 from '../../GuanKiann/分享鍵/分享鍵';
import 後端 from '../../後端';
import Debug from 'debug';
import Promise from 'bluebird';
var superagent = require('superagent-promise')(require('superagent'), Promise);

var debug = Debug('itaigi:Kong無關鍵字');

export default class 無關鍵字 extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      newWordsLess: [],
      newWordsMore: [],
      isShowMore: false,
    };

    this.onShowMoreClick = () => {
      this.setState({
          isShowMore: !this.state.isShowMore,
        });
    };
  }

  componentDidMount() {
    superagent.get(後端.揣上新貢獻的外語())
        .then(({ body }) => {
          const newWords = body.列表.map(item => item.外語資料);
          const newWordsLess = newWords.slice(0, 20);
          const newWordsMore = newWords.slice(0, 80);
          this.setState({
            newWordsLess,
            newWordsMore,
          });
        });
  }

  render() {
    return (
      <div className='ui left aligned container'>
        <br/>
        <header>
          <h1>iTaigi愛台語</h1>
          <p>一部集結群眾編纂的開放台語辭典</p>
        </header>

        <br/>
        <h2>維修公告</h2>
        <table className='ui celled striped table'>
          <caption style={{'textAlign': 'left'}}>維修公告紀錄:</caption>
          <thead>
            <tr><th>日期</th><th>事項</th></tr>
          </thead>
          <tbody>
            <tr><td>2024.11.10</td><td>更新外部超連結網址及名稱。</td></tr>
            <tr><td>2024.11.7</td><td>修正iPhone、iPad聲音播放問題。</td></tr>
            <tr><td>2024.3.28</td><td>由於人力不足難以配合Facebook審查機制，登入具名貢獻功能暫且下架。</td></tr>
            <tr><td>2023.11.13</td><td>由於貢獻紀錄參雜許多腥羶內容與中國惡意廣告，我很會、燒燙燙新詞暫且下架。</td></tr>
          </tbody>
        </table>
        <br/>
        <FBTest/>
      </div>
    );
  }
}
