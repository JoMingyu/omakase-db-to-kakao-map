# Omakase DB to KaKao Map
[전국 오마카세 스시야 DB](https://docs.google.com/spreadsheets/d/1BQqkb4NLZ0v2Ml1gAfamEqx9mie5MwZLCUbGH8IiUHE/edit#gid=0) 데이터를 가지고 KaKao Map에 북마크를 추가하는 스크립트

<img width="1000" alt="스크린샷 2021-06-18 오후 9 53 32" src="https://user-images.githubusercontent.com/21031883/122566568-a22b3a80-d082-11eb-892d-233d8b817a21.png">
<img width="350" alt="스크린샷 2021-06-18 오후 10 14 15" src="https://user-images.githubusercontent.com/21031883/122566482-8a53b680-d082-11eb-8062-6b73cd450623.png">

## 1차 공유
- 디너 ~50,000원 : [http://kko.to/x3YOP8ofM](http://kko.to/x3YOP8ofM)
- 디너 50,001원 ~ 100,000원 : [http://kko.to/lFnhg5ofo](http://kko.to/lFnhg5ofo)
- 디너 100,001원 ~ 150,000원 : [http://kko.to/PBpbP8B4M](http://kko.to/PBpbP8B4M)
- 디너 150,001원 ~ 200,000원 : [http://kko.to/5V-sP5Bfo](http://kko.to/5V-sP5Bfo)
- 디너 200,001원 ~ 250,000원 : [http://kko.to/qOXbg8o4p](http://kko.to/qOXbg8o4p)
- 디너 250,001원 ~ 300,000원 : [http://kko.to/bCCsP8o4p](http://kko.to/bCCsP8o4p)
- 디너 300,000원 ~ : [http://kko.to/dkS2g8B4p](http://kko.to/dkS2g8B4p)
- 미분류 : [http://kko.to/AC9pE5B4o](http://kko.to/AC9pE5B4o)

## 사용법
1. `pipenv install`
2. `run.py` 가서 `map=KaKaoMap(token="...")` 부분 채우기. 카카오맵에서 네트워크 탭 열고, 아무 API 호출이나 만든 뒤 Cookie 헤더로 날아가는 `_kawlt=...` 부분 뜯어다가 붙여넣으면 됩니다.
3. `folders` 인자를 통해 폴더들에 스시야가 들어가는 조건을 명시할 수 있습니다.
