import React from 'react';
import Debug from 'debug';

var debug = Debug('itaigi:LaiLik');

export default class LaiLik extends React.Component {
  tshuttshu() {
    console.log("this.props.貢獻者", this.props.貢獻者)
    if (this.props.guagi == "奇異果") {
      if(this.props.貢獻者 == '沒有人'){
         return (
          <span>理由：從小就聽長輩這樣說。</span>
          )
      }
      else if(this.props.貢獻者 == 'Morrison Iûnn'){
        return <span>理由：參考桃子形狀發想的詞。</span>
      }
    }
  }
  render() {
    return (
    <div className='content'>
      <span>出處：{this.props.貢獻者}</span><br/>
      {this.tshuttshu()}
      {/*<ul>
      <li></li>
      <li>像是猴子臉部</li>
      </ul>*/}
    </div>
    );
  }
}
