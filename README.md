# iTaigi 愛台語

[![Build Status](https://app.travis-ci.com/i3thuan5/itaigi.svg?token=waFyTE3XbanfxopdQkua&branch=main)](https://app.travis-ci.com/i3thuan5/itaigi)
[![devDependency Status](https://david-dm.org/i3thuan5/itaigi/dev-status.svg)](https://david-dm.org/i3thuan5/itaigi?type=dev)
[![made in taiwan](https://img.shields.io/badge/made%20in-taiwan-blue.svg)](https://itaigi.tw)
[![made in g0v](https://img.shields.io/badge/made%20in-g0v-B81C21.svg)](http://g0v.tw/en-US/)

* [itaigi網站](https://itaigi.tw)
* [FB粉專](https://www.facebook.com/ukauitaigi/)
* [Slack討論](https://g0v-tw.slack.com/messages/itaigi/)
* [萌典松](http://moe.kktix.cc/)
* [專案Hackpad](https://g0v.hackpad.tw/moed7ct-taigi-neologism)
* [API介面](http://docs.tai5uan5gian5gi2phing5thai5.apiary.io/#)
* [正規化工作表](https://docs.google.com/spreadsheets/d/1_sXX2CGJsfSUTg-r-RGc4ApU1fPUmuLc2DmUSy4y_Zk)
* [例句API](https://github.com/i3thuan5/itaigi-LeKu)
* [名姓API](https://github.com/i3thuan5/itaigi-MiaSenn)

## Run

```bash
cd tsiantuan/
npm ci
npm run start
```

Then open <http://localhost:3000/>

### Nodejs installation (optional)

可使用[nvm](https://github.com/nvm-sh/nvm)安裝nodejs，請安裝nodejs版本16。

```bash
curl ...
nvm install 16
nvm use 16
```

### Backend

[Wiki](https://github.com/g0v/itaigi/wiki)

```bash
zcat TSULIAUKHOO.sql.gz | docker-compose exec -T postgres psql -U postgres
```

## 更新、上線

```bash
git pull
docker compose build --pull
docker compose pull
docker compose up -d
docker compose exec gunicorn python manage.py migrate
```

Hó-sè.

## License

MIT License <http://g0v.mit-license.org/>
