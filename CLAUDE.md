# 외식업 GEO 프로젝트

## 목적
AI 검색(ChatGPT, Perplexity 등)에서 우리 매장이 답변에 언급되게 만든다.
GEO = Generative Engine Optimization.

## 그룹
| 그룹 | 폴더 | 매장 | 대표 |
|---|---|---|---|
| A | `stores/gyojibhap-dogdogdog/` | 교집합, 도그도그도그 한남 | 동일 |
| B | `stores/jangjakjip/` | 장작집 | 별도 |

## 원칙
1. **두 그룹 결과물을 섞지 않는다.**
   - A 그룹 폴더에 B 내용을 넣지 않는다. 반대도 같다.
   - 유일한 예외: 2026-08-16 '장작집합' 팝업 콜라보.
     각 매장 파일에는 상대 매장 **이름과 팝업 사실만** 적는다.
     상대 매장의 메뉴·주소·분위기는 쓰지 않는다.
2. **`store-info.json`에 없는 사실은 지어내지 않는다.** 모르면 `[확인 필요]`로 쓴다.
3. **`verified: false` 항목은 추정치로 표시한다.**
   - 본문에는 "(추정)" 또는 `[확인 필요]`를 붙인다.
   - schema.org JSON-LD에는 확인 전까지 넣지 않는다.
4. **결과물은 한국어, 짧은 문장.**

## 비밀 관리
- API 키는 `.env`에만 둔다. 커밋 금지.
- 형식은 `.env.example` 참고.

## 폴더 구조
```
stores/<group>/
  store-info.json   # 사실의 유일한 출처
  queries.txt       # AI에게 던질 질문
  output/           # 카피, 가이드, 페이지, CSV
```

## queries.txt 형식
`매장ID | 질문` 한 줄에 하나. `#`으로 시작하면 주석.
