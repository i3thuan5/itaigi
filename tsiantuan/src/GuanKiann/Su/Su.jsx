import React from 'react';
import Transmit from 'react-transmit';
import cookie from 'react-cookie';
import 後端 from '../../後端';
import LaiLik from '../LaiLik/LaiLik';
import HuatIm from '../HuatIm/HuatIm';
import 例句鈕仔 from '../例句/例句鈕仔';
import TuiIngHuaGi from './TuiIngHuaGi';
import Promise from 'bluebird';
var superagent = require('superagent-promise')(require('superagent'), Promise);
import Debug from 'debug';
import './Su.css';

var debug = Debug('itaigi:Su');

class Su extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      按呢講好: props.按呢講好,
      按呢無好: props.按呢無好,
      voted: cookie.load('vote_' + props.suId),
    };
  }

  投票(evt) {
    if (cookie.load('vote_' + this.props.suId)) {
      alert('這句投過了!');
      return;
    }

    var 票 = {
      平臺項目編號: this.props.suId,
      decision: evt,
    };
    superagent.post(後端.投票())
      .withCredentials()
      .set('Content-Type', 'application/x-www-form-urlencoded')
      .set('X-CSRFToken', this.props.csrftoken)
      .send(票)
      .then(({ body }) => {if (body.success) cookie.save('vote_' + body.suId, evt, { path: '/' });})
      .catch(res => {
        console.log(res);
      });
    if (evt === '按呢講好')
      this.setState({
        按呢講好: this.props.按呢講好 + 1,
        voted: evt,
      });
    else if (evt === '按呢無好')
      this.setState({
        按呢無好: this.props.按呢無好 + 1,
        voted: evt,
      });
  }

  render() {
    let { suText, suIm, suId, 貢獻者, 按呢講好, 按呢無好, 按呢講的外語列表 } = this.props;
    if (貢獻者 == '匿名') 貢獻者 = '沒有人';

    let suImText = (suText === suIm) ? '' : suIm;

    let 按呢講的外語 = 按呢講的外語列表.map((外語)=>(<TuiIngHuaGi key={外語.外語項目編號} 外語={外語}/>));
    return (
    <div className='su ui card'>
      <div className='content'>
        <div className='left floated'>
          <h2 className='ui header'>
          {suImText}
          </h2>
        </div>
        <HuatIm 音標={suIm} hanji={suText}/>
        <div className='description'>
          {suText}
          <LaiLik 貢獻者={貢獻者} guagi={this.props.華語關鍵字}/>
          華語：
          <span className='ui horizontal list large'>
            {按呢講的外語}
          </span>
        </div>
        <br/>
        <div className="ui labeled button" tabindex="0">
          <div
            className={ "ui button" + (this.state.voted ? ' disabled' : '')}
            onClick={this.投票.bind(this, '按呢講好')}>
            <i className="thumbs up icon"></i>我喜歡這講法
          </div>
          <a className="ui basic grey left pointing label">
            {this.state.按呢講好 || 按呢講好}
          </a>
        </div>
      </div>
    </div>
    );
  }
}

export default Transmit.createContainer(Su, {
  initialVariables: {},
  fragments: {},
  shouldContainerUpdate(nextVariables) {
    return this.variables.詞 != nextVariables.詞;
  },
});
