import React from 'react';
import ToLam from '../GuanKiann/ToLam/ToLam';
import 分享鍵 from '../GuanKiann/分享鍵/分享鍵';

export default class FBTest extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      href: '',
    };
  }

  /*
  componentDidMount() {
    var _this = this;
    window.fbAsyncInit = function () {
      FB.init({
        appId: '252264671778664',
        xfbml: true,
        version: 'v2.5',
      });

      FB.getLoginStatus(function (response) {
        FB.api('/ukauitaigi/feed', function (feed) {
          var postID = feed.data[0].id.split('_')[1];
          FB.api('/' + postID + '?fields=source', function (photo) {
            _this.getFacebookResponse(photo);
          });
        });
      });

    }.bind(this)

    ;(function (d, s, id) {
      var js;
      var fjs = d.getElementsByTagName(s)[0];
      if (d.getElementById(id)) {return;}

      js = d.createElement(s); js.id = id;
      js.src = '//connect.facebook.net/en_US/sdk.js';
      fjs.parentNode.insertBefore(js, fjs);
    }(document, 'script', 'facebook-jssdk'));
  }
  */

  renderFacebookResponse() {
    return (
    <div className='kong content'>
      <div className='ui basic segment container'>
        <p className='ui header'>快分享 iTaigi 給你的朋友知道吧！</p>
        <分享鍵 size='large' pathname={ '' }/>
      </div>
      <br/>
    </div>
    );
  }

  getFacebookResponse(photo) {
    this.setState({ href: 'http://facebook.com/' + photo.id, src: photo.source });
  }

  render() {
    return (
      <div>
        <div className='container'>
          {this.renderFacebookResponse()}
        </div>
      </div>
    );
  }
}
