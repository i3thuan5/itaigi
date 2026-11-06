import React from 'react';
import ToLam from '../GuanKiann/ToLam/ToLam';
import IapKha from '../GuanKiann/IapKha/IapKha';
import 後端 from '../後端';
import 例句表 from '../GuanKiann/例句/例句表';
import 載入頁面 from '../GuanKiann/載入頁面/載入頁面';
import { gaLeKu } from '../GA';
import { oomiatuann } from './OoMiaTuann';
import './App.css';
import { Promise } from 'bluebird';
import { browserHistory, Link } from 'react-router';

var superagent = require('superagent-promise')(require('superagent'), Promise);
import Debug from 'debug';
var debug = Debug('itaigi:App');

export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = { csrftoken: '' };
    this.看csrftoken();
  }

  看csrftoken() {
    superagent.get(encodeURI(後端.網址() + 'csrf/看'))
        .withCredentials()
        .then(({ body }) => (this.setState({ csrftoken: body.csrftoken }), null))
        .catch((err) => (debug(err)));
  }

  查怎樣講(外語) {
    let pitui_oomia_tin = [];
    if(外語) {
      pitui_oomia_tin = oomiatuann.filter(substr => 外語.includes(substr));
    }
    if(外語 && 外語.length < 10 && pitui_oomia_tin.length == 0) {
      browserHistory.replace('/k/' + 外語);
    }
    else {
      browserHistory.replace('/');
    }
  }

  開例句(外語, 漢字, 台羅) {
    browserHistory.replace(
      '/k/' + encodeURIComponent(外語) +
      '/' + encodeURIComponent(漢字) +
      '/' + encodeURIComponent(台羅)
      );
    gaLeKu(漢字, 台羅);
  }

  關例句(外語) {
    this.查怎樣講(外語);
  }

  render() {
    const { k, han, lo } = this.props.params;
    return (
    <div className='app background'>
      <header className='app header'>
        <ToLam pathname={this.props.location.pathname}/>
      </header>
      <Link className='app header-kongko' to='/tshutsiaua'>
        🚀「厝鳥仔講台語」口說跟讀練習APP上架啦！🔥 立即下載輕鬆開喙說台語！
      </Link>
        { React.cloneElement(
          this.props.children,
          {
            查怎樣講: this.查怎樣講.bind(this),
            csrftoken: this.state.csrftoken,
            開例句: this.開例句.bind(this),
            variables: { 關鍵字: k },
            renderLoading: <載入頁面/>,
          }
        )}
      <例句表 關例句={this.關例句.bind(this, k)}
         漢字={han} 台羅={lo}
         variables={{ 漢字: han, 台羅: lo }}/>
      <IapKha/>
    </div>
    );
  }
}

App.propTypes = {
  history: React.PropTypes.object,
  children: React.PropTypes.object,
};
