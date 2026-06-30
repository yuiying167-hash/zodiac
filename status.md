# Status — 2026-06-30

## 변경 내용

### 광고 구조 정리 (수동 슬롯 → Auto Ads 전환)
- **문제**: zodiac.spattra.com에 Google AdSense 광고 미송출 (Auto Ads + 앵커 광고 모두 안 됨)
- **원인 추정**: `<head>`의 Auto Ads 스크립트와 수동 `<ins>` 광고 슬롯 3개(index.html) + 3개(posts/*.html)가 충돌. 특히 `display:none` 상태의 사이드레일 광고에서 `adsbygoogle.push()` 호출이 전체 AdSense 초기화에 영향을 줌
- **수정**:
  - `index.html`: 사이드레일 광고 2개 + 중간 광고 1개 제거, `side-rail` CSS 제거
  - `generator.py`: 상/중/하 광고 3개 제거, `.ad-box`/`.ad-label` CSS 제거
  - `posts/*.html` 432개: 수동 광고 슬롯 3개씩 전량 제거
- **결과**: `<head>`의 Auto Ads 스크립트만 남음 (Cloudflare 배포 후 광고 송출 확인 필요)

### 신규 파일
- `agent.md` — 프로젝트 기술 문서 (AI 에이전트용)

## 미해결
- 광고 송출 여부는 Cloudflare 배포 완료 후 실제 사이트에서 확인 필요
- 만약 계속 안 나오면 AdSense 대시보드에서 zodiac.spattra.com 승인 상태 확인
