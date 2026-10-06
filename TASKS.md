# TASKS

공통: CLAUDE.md 원칙을 따른다. 그룹별로 따로 작업한다.

## 0. 확인 요청
`verified: false` 항목을 사장님께 확인받는다. 확인되면 `true`로 바꾸고 `[확인 필요]`를 지운다.

- [ ] 교집합: 인스타 @gyojibhap_itaewon
- [ ] 교집합: 주소, 영업시간, 전화, 대표 메뉴, 가격대 (전부 [확인 필요])
- [ ] 도그도그도그 한남: 주소, 브레이크타임 없음, 반려견 동반, 포장·배달, 주차 불가
- [ ] 도그도그도그 한남: 영업시간, 전화, 대표 메뉴, 가격대 (전부 [확인 필요])
- [ ] 장작집: 연남 본점, 주소, 누룽지 통닭·돼지갈비·생맥주, 예약 가능, 주차 가능
- [ ] 장작집: 영업시간, 전화, 가격대 (전부 [확인 필요])
- [ ] 장작집합 팝업: 날짜 2026-08-16이 이미 지남. 진행 여부·장소·후속 일정 확인

## 1. 플랫폼 카피
매장별로 `output/platform-copy.md` 작성.
- [ ] 네이버 플레이스 소개글
- [ ] 카카오맵 소개글
- [ ] 인스타 바이오
- [ ] 구글 비즈니스 프로필 설명
- 한 문장 소개를 기준 문구로 쓴다.

## 2. 블로거 가이드
그룹별로 `output/blogger-guide.md` 작성.
- [ ] 방문 전 알려줄 사실 (verified:true만)
- [ ] 쓰면 안 되는 표현 (지어낸 사실)
- [ ] 추천 키워드 (queries.txt 기준)
- [ ] 사진 촬영 요청 포인트

## 3. 매장별 원페이지 + JSON-LD + FAQ
`python3 tools/build_site.py` 실행. `store-info.json`에서 페이지를 만든다.
출력: `stores/<group>/output/site/<store-id>/index.html`
- [x] 한 페이지 소개 (짧은 문장)
- [x] schema.org `Restaurant` JSON-LD (verified:true 값만)
- [x] FAQ + `FAQPage` JSON-LD (verified:true 답변만)
- [x] GitHub Pages 워크플로 (`.github/workflows/pages.yml`, 그룹별 경로 분리)
- [ ] 저장소 Settings > Pages > Source를 "GitHub Actions"로 설정 (사람이 해야 함)
- [ ] 배포 후 Rich Results Test로 검증
- [ ] 0번 확인 후 `verified`를 true로 바꾸고 다시 빌드

배포 주소: `/<group>/<store-id>/`
- `/gyojibhap-dogdogdog/gyojibhap/`
- `/gyojibhap-dogdogdog/dogdogdog/`
- `/jangjakjip/jangjakjip/`

## 4. AI 노출 측정
OpenAI·Perplexity API로 `queries.txt` 질문을 던진다. 답변에 매장이 언급됐는지 기록한다.
- [ ] 스크립트 작성 (키는 `.env`에서 읽기)
- [ ] 그룹별로 따로 실행
- [ ] `output/mentions-YYYY-MM-DD.csv` 저장
- CSV 열: `date, engine, store_id, query, mentioned, excerpt, citations`
- [ ] 월 1회 반복해 추이 확인
