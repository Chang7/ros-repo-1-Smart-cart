# Smart Office Robot Service

ROS 2 기반 사무실 안내/배송 로봇 서비스 프로젝트입니다.  
`main_server`, `ai_server`, `robot` 런타임을 분리해 여러 로봇과 AI 추론 서버를 연동하는 구조를 목표로 합니다.

## 주요 구성

- `main_server/`
  - FastAPI 기반 중앙 서버
  - 사용자/관리자 API, 로봇 상태 관리, 작업 시나리오 관리
  - DB repository, AI gRPC client, ROS bridge 연동 계층 포함
- `ai_server/`
  - gRPC 기반 AI 서버
  - LLM 의도 분석, Vision 추론, UDP 영상 수신 구조 포함
  - Qwen/Ollama, YOLO, 얼굴 인식 연동을 위한 서비스 계층 포함
- `robot/`
  - ROS 2 Jazzy 워크스페이스
  - 로봇 executor, bringup, safety, communication node, rosbridge launch 포함
- `tests/`, `main_server/test_scripts/`
  - gRPC, 시나리오, map/route 관련 테스트 스크립트
- `Docs/`
  - 설계/구현 가이드 문서

## 빠른 시작

### 1. Python 서버 의존성 설치

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 환경 변수 설정

```bash
cp .env.example .env
```

주요 변수:

- `SERVER_HOST`, `SERVER_PORT`
- `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `DB_PORT`
- `ROS_BRIDGE_HOST`, `ROS_BRIDGE_PORT`
- `LLM_GRPC_HOST`, `LLM_GRPC_PORT`
- `VISION_GRPC_HOST`, `VISION_GRPC_PORT`
- `VIDEO_STREAM_HOST`, `VIDEO_STREAM_PORT`
- `LLM_MODEL_NAME`

### 3. AI 서버 실행

```bash
python -m ai_server.server
```

분리 실행 구조를 사용할 경우:

```bash
python ai_server/scripts/start_separated_servers.py
```

### 4. Main 서버 실행

```bash
uvicorn main_server.app:app --host 0.0.0.0 --port 8000 --reload
```

### 5. Robot 런타임 실행

ROS 2 Jazzy 환경에서:

```bash
cd robot/jazzy_ws
colcon build --symlink-install
source install/setup.bash

ros2 launch office_robot_bringup bringup.launch.py \
  robot_ns:=robot01 robot_id:=1 enable_rosbridge:=true
```

## 개발 상태 요약

현재 `dev` 브랜치는 전체 아키텍처와 주요 모듈 구조가 상당 부분 들어가 있지만, 완성도를 높이려면 다음 작업이 필요합니다.

1. README/문서 인코딩 및 실행 가이드 정리
2. `.env.example` 공백/변수명 정규화
3. AI 서버의 mock/stub 로직과 실제 모델 연동 경계 명확화
4. FastAPI 서버 최소 smoke test 추가
5. ROS 패키지별 launch/test 절차 정리
6. DB 스키마/초기 데이터 문서화
7. CI에서 Python lint/test 범위 정의

자세한 개발 우선순위는 `DEVELOPMENT_PLAN.md`를 참고하세요.

## 주의사항

- `.env`, DB 비밀번호, API key, SSH key 등 민감정보는 커밋하지 마세요.
- ROS 2 빌드 산출물인 `build/`, `install/`, `log/`는 로컬 산출물이므로 Git에 올리지 않습니다.
- 실제 로봇 연결 전에는 `mock_mode` 또는 테스트 스크립트로 먼저 검증하는 것을 권장합니다.
