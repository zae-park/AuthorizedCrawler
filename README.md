# 자동 로그인 & 웹 스크래핑

로그인이 필요한 url에서 crawling하기.

### `Status Table`

| name        | data root                        | status       |
|-------------|----------------------------------|--------------|
| 네이버 스마트 스토어 | 판매관리/배송현황 관리 & 구매확정 내역           | `Done`       |
| 카카오 톡스토어    | 판매관리/통합 주문 관리 + 정산관리/구매결정 상세     | `WIP`  |
| 쿠팡 서플라이 허브  | 애널리틱스/판매-일간종합 성과 지표 + 물류/입고상세내역  | Yet          |
| 쿠팡 윙        | 정산/매출내역                          | Yet          |
| 파트너 컬리      | 입고관리/[공급사]입고확정내역                 | Yet          |

### configration
`root/config/url_info.json`에 스크래핑하려는 url과 계정 정보를 설정하면 스크래핑 가능.


---
## Captcha 피하기

![naver captcha](https://cdn.digitaltoday.co.kr/news/photo/202009/247582_214051_3626.jpg)

셀레니움의 send_keys를 통해 id, pw 란에 계정정보를 입력하는 경우 naver에서 bot으로 인식하여 captcha 인증을 거쳐야 함.
대신, clipboard에 계정 정보를 저장한 후 붙여넣는 방식으로 입력하면 이를 우회할 수 있음.

