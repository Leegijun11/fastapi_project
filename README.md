# FastAPI Project

이 프로젝트는 **FastAPI**와 **Alembic**을 활용한 백엔드 서버 프로젝트입니다. 효율적인 DB 마이그레이션과 구조화된 API 아키텍처를 기반으로 구축되었습니다.

---

## 주요 기능
- **FastAPI 기반**: 비동기 처리를 지원하는 고성능 API 서버
- **Alembic 마이그레이션**: 데이터베이스 스키마 버전 관리 및 자동 마이그레이션 지원
- **JWT 인증**: `auth.py` 및 `jwt_handle.py`를 통한 보안 및 토큰 기반 인증
- **계층화된 구조**: CRUD, Service, Router 계층 분리를 통한 유지보수성 향상

## 기술 스택
- **Framework**: FastAPI
- **Database Migration**: Alembic
- **Validation**: Pydantic
- **Security**: JWT (JSON Web Token)
- **Server**: Uvicorn

## 프로젝트 구조
```text
.
├── alembic/              # DB 마이그레이션 환경 설정 및 히스토리
├── backend/              # 메인 애플리케이션 소스 코드
│   ├── crud/             # 데이터베이스 CRUD 로직
│   ├── models/           # 데이터베이스 테이블 정의
│   ├── router/           # API 엔드포인트(라우터) 정의
│   ├── schemas/          # Pydantic 데이터 스키마 (DTO)
│   ├── service/          # 비즈니스 로직 처리
│   ├── auth.py           # 사용자 인증 로직
│   ├── database.py       # DB 연결 및 세션 설정
│   ├── jwt_handle.py     # JWT 토큰 생성 및 검증
│   ├── middleware.py     # 미들웨어(CORS, 로깅 등) 설정
│   ├── settings.py       # 환경 설정(Config)
│   └── requirements.txt  # 내부 의존성 목록
├── .gitignore            # Git 제외 파일 설정
├── alembic.ini           # Alembic 설정 파일
├── main.py               # 애플리케이션 실행 진입점
└── requirements.txt      # 프로젝트 전체 의존성 목록


## 설치 및 실행 방법

### 1. 저장소 복제 및 가상환경 설정
```bash
# 저장소 복제
git clone [https://github.com/Leegijun11/fastapi_project.git](https://github.com/Leegijun11/fastapi_project.git)
cd fastapi_project

# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
.\venv\Scripts\activate

# 필요한 패키지 설치
pip install -r requirements.txt

# 서버 실행
uvicorn main:app --reload


## API 문서 확인 및 테스트
FastAPI에서 제공하는 자동 문서 기능을 통해 별도의 도구 없이 API를 테스트할 수 있습니다.

### Swagger UI: http://127.0.0.1:8000/docs

대화형 인터페이스를 통해 실시간으로 API 요청을 보내고 응답을 확인할 수 있습니다.

## 주요 모듈 상세 설명
backend/auth.py & jwt_handle.py: 사용자 로그인 시 비밀번호 검증과 JWT 토큰 발행, 그리고 보안이 필요한 API 접근 시 토큰 유효성 검사를 수행합니다.

backend/crud/: 데이터베이스에 직접 접근하는 코드들로, 다른 모듈에서 DB 작업을 수행할 때 호출하는 인터페이스 역할을 합니다.

backend/middleware.py: 모든 요청(Request)이 서버에 도달하기 전이나 응답(Response)이 나가기 전에 처리되는 로직(예: CORS 허용 범위 설정)을 담고 있습니다.

main.py: FastAPI 인스턴스를 생성하고 각 router를 앱에 연결(Include)하며 서버의 시작점이 됩니다.






