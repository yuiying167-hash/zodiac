# zodiac.spattra.com — Agent Guide

## 프로젝트 개요

태국어 12띠 궁합 (Zodiac Love Match) 정적 사이트 생성기. Claude AI로 콘텐츠를 생성하고 HTML 파일로 빌드하여 Cloudflare에 배포.

- 도메인: https://zodiac.spattra.com
- 저장소: https://github.com/yuiying167-hash/zodiac
- 호스팅: Cloudflare (GitHub 연동, Auto Deploy)

## 파일 구조

```
zodiac-spattra/
├── generator.py        # 메인 생성기 (Claude AI + HTML 조립)
├── index.html          # 홈페이지 (띠 선택 인터랙티브 UI)
├── add_sns.py          # SNS 공유 버튼 일괄 삽입
├── debug_sns.py        # SNS 버튼 디버깅 스크립트
├── update_year.py      # 저작권 연도 일괄 변경
├── ads.txt             # Google AdSense 설정
├── sitemap.xml         # 사이트맵
└── posts/              # 생성된 궁합 페이지들 (432개 = 12x12x3)
```

## 핵심 로직 (generator.py)

### 데이터
- 12 띠: rat, ox, tiger, rabbit, dragon, snake, horse, goat, monkey, rooster, dog, pig
- 3 성별 조합: mf (남녀), mm (남남), ff (여여)
- 점수: 91~99점 (seed 기반 고정, API 호출 불필요)

### 콘텐츠 생성
- Claude 3 Haiku API로 각 커플 조합별 태국어 연애 분석 생성
- 프롬프트는 태국인 점성가 역할, 600자 이상, HTML 구조 고정
- `API_KEY = "your_key"` — 실행 전에 실제 키로 교체 필요
- 이미 생성된 파일이 있으면 스킵 (멱등성 보장)

### HTML 템플릿
- 다크 테마 (glass morphism 디자인)
- 점수 원형 게이지, 등급(S/A+/A), 분석글, 팁
- 구글 폰트 Sarabun, Font Awesome 아이콘
- Google AdSense Auto Ads만 사용 (수동 슬롯 없음)

## 배포

GitHub에 푸시하면 Cloudflare Pages가 자동 배포.

```bash
git add -A
git commit -m "message"
git push origin main
```

## 유틸리티 스크립트

| 스크립트 | 용도 | 실행 |
|---------|------|------|
| `add_sns.py` | posts/*.html 에 SNS 공유 버튼 추가 | `python add_sns.py` |
| `debug_sns.py` | SNS 버튼 디버깅 (중복 체크, 강제 삽입) | `python debug_sns.py` |
| `update_year.py` | 저작권 연도 2024→2026 변경 | `python update_year.py` |

## 광고

- Google AdSense Auto Ads만 사용 (앵커 광고 포함)
- Publisher ID: `pub-3198582468837090`
- `<head>`에 Auto Ads 스크립트 1개만 있음
- AdSense 계정에서 spattra.com 전체 도메인에 Auto Ads 활성화됨
- zodiac.spattra.com에 광고 미송출 시: Cloudflare Rocket Loader, Worker 충돌, 또는 AdSense 사이트 승인 상태 확인

## 주의사항

- `generator.py` 실행 전 `API_KEY` 반드시 설정
- posts/ 는 Git에 포함됨 (대량 파일 주의)
- sitemap.xml 은 generator.py에서 자동 생성 안 함 — 별도 관리 필요
