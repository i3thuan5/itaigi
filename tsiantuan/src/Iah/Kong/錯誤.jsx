import React from 'react';
import 分享鍵 from '../../GuanKiann/分享鍵/分享鍵';
import Debug from 'debug';

var debug = Debug('itaigi:Kong錯誤');

export default class 錯誤 extends React.Component {
  render() {
    return (
    <div className='kong content'>
      <div className='ui segment'>
        <h3>找「{this.props.華語關鍵字}」錯了嗎？</h3>
        {this.props.內容}
    </div>
    );
  }
}
