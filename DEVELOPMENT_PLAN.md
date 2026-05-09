# Development Plan

이 문서는 `dev` 브랜치를 실제 시연/재업로드 가능한 상태로 정리하기 위한 우선순위 목록입니다.

## 1. 즉시 개선할 항목

- 깨진 README/문서 인코딩 정리
- 실행 진입점 문서화
  - `ai_server.server`
  - `main_server.app`
  - ROS 2 bringup launch
- `.env.example` 변수명 정리
- 로컬 개발용 실행 순서 문서화

## 2. Main Server

- FastAPI app import smoke test 추가
- DB 연결 실패 시 mock 또는 명확한 에러 메시지 제공
- API route 목록 문서화
- 로봇/작업 repository interface와 MySQL 구현체 연결 상태 점검

## 3. AI Server

- LLM service의 TODO/mock 로직 구분
- Vision service의 입력/출력 schema 문서화
- UDP video receiver의 예외 처리와 종료 처리 점검
- gRPC proto 재생성 절차 문서화

## 4. Robot Runtime

- ROS 2 Jazzy 기준 패키지별 build/test 명령 정리
- `mock_mode` 실행 예제 추가
- safety node, executor node의 runtime contract 정리
- camera/UDP bridge systemd 배포 절차 정리

## 5. 테스트/CI

- Python 서버 모듈 import test
- FastAPI route smoke test
- gRPC mock server/client test
- ROS 패키지는 별도 Ubuntu/ROS 환경에서 CI 가능 여부 검토

## 6. GitHub 재업로드 전 체크리스트

- `git status` clean 확인
- `.env`, DB dump, 개인 IP/토큰 제거
- README 실행 명령 검증
- 최소 smoke test 통과
- `dev` 또는 별도 작업 브랜치로 push
