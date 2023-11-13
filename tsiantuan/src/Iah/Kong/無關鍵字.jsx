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
      <div className='kong content'>
        <FBTest/>
      </div>
    );
  }
}
