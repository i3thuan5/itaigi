import React from 'react';
import { Link } from 'react-router';

class About extends React.Component {
  render() {
    return (
    <div className='main ui text container'>
      <div className='about' style={{fontSize: "1.2rem", paddingTop: "20px", paddingBottom:"20px"}}>
        <h1>關於本站</h1>
        <p>
          iTaigi愛台語-群眾台語辭典是g0v零時政府專案
          <a target='_blank' href='https://moedict.tw'>「萌典」</a>
          的延伸辭典，想知道一個詞的台語怎麼說，來這裡查就對了！甚麼都可以查，但不一定查得到，查不到時可以發問，或者自己發明台語講法貢獻給大家，簡單說就是「自己的辭典自己編」。
        </p>

        <section style={{marginBottom:"20px"}}>
        <h2>如何查詢辭典</h2>
        <ul>
          <li><p style={{lineHeight: "1.8rem"}}>在<Link to='/k'>「查辭典」</Link>查詢框中輸入想查的「華語詞」，按下「查辭典」，會出現各種講法。</p></li>
          <li><p style={{lineHeight: "1.8rem"}}>每一個對應的台語詞目是一張獨立的卡片，顯示發音 play 鍵、出處及該台語詞其他的對應華語。</p></li>
          <li><p style={{lineHeight: "1.8rem"}}>如果覺得這個講法不錯，可以點「按呢講好」來投贊成票，如果覺得這個翻譯不是很妥當，可以點「按呢怪怪」投疑慮票。</p></li>
          <li><p style={{lineHeight: "1.8rem"}}>這些詞彙的排列順序會依投票結果來呈現，使用者可參考投票結果選用詞彙。</p></li>
        </ul>
        </section>

        <section style={{marginBottom:"20px"}}>
        <h2>正規化團隊</h2>
        <p style={{lineHeight: "1.8rem"}}>
          除了一般使用者，我們也需要熟悉教育部台語漢字和臺羅的朋友，一起加入正規化團隊，有意者請私訊
          <Link target='_blank' to='https://www.facebook.com/ukauitaigi'>iTaigi FB 粉專</Link>。
        </p>
        </section>

        <section style={{marginBottom:"20px"}}>
        <h2>合作單位</h2>
        <p style={{lineHeight: "1.8rem"}}>
          本網站的語音合成服務由
          <a href='https://ithuan.tw/'>意傳科技</a>的台灣媠聲計劃提供，台灣媠聲接受
          <a href='https://www.moc.gov.tw/'>文化部</a>語言多樣性友善環境補助。
        </p>
        <img
            src='https://file.moc.gov.tw/001/Upload/OldFiles/AdminUploads/mochistory/images/download/logo/moc/moc_logo1.png'
            width='300px' />
        </section>
      </div>
    </div>
    );
  }
}

// About.propTypes = {
//   params: React.PropTypes.object,
//   查怎樣講: React.PropTypes.func,
// };
export default About;
