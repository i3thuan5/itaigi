import React from 'react';
import Tshue from '../../GuanKiann/Tshue/Tshue';
import 其他建議 from './其他建議';
import 分享鍵 from '../../GuanKiann/分享鍵/分享鍵';
import 留言板 from '../../GuanKiann/留言板/留言板';
import Debug from 'debug';

var debug = Debug('itaigi:Kong無結果');

export default class 無結果 extends React.Component {
  render() {
    return (
      <div className='tshueBo'>
         <div className='分享'>
           <span>「{ this.props.華語關鍵字 }」的台語要怎麼說呢？來考考你的朋友吧！</span>
           <分享鍵 pathname={this.props.pathname}/>
        </div>

      <其他建議
        內容={this.props.內容}
        華語關鍵字={this.props.華語關鍵字}
        開例句={this.props.開例句.bind(this)}/>

        <h3 className='ui horizontal divider header'>
          <i className='outline comments icon'></i>
          來討論
          「<span className='ui pink header'>{this.props.華語關鍵字}</span>」
        </h3>
        <留言板 />
      </div>
    );
  }
}
