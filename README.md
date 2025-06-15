# Ad 프로젝트

이 저장소는 **Django 5**로 작성된 간단한 Q&A 웹 애플리케이션입니다. 회원 가입과 로그인 기능을 제공하며, 질문 등록과 답변 및 댓글 작성, 추천 기능 등을 지원합니다. 기본 설정은 PostgreSQL 데이터베이스를 사용하도록 구성되어 있습니다.

## 주요 기능

- 사용자 인증 (회원 가입, 로그인, 로그아웃)
- 질문 작성, 수정, 삭제
- 답변과 댓글 작성
- 질문과 답변 추천 기능
- 인증 뷰에 대한 간단한 테스트 코드 포함

## 빠른 시작

1. Python 3.11 이상을 설치합니다.
2. 필요한 패키지를 설치합니다.
   ```bash
   pip install -r requirements.txt
   ```
3. `config/settings.py` 파일의 데이터베이스 설정을 환경에 맞게 수정합니다.
4. 마이그레이션을 적용하고 개발 서버를 실행합니다.
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```
5. 브라우저에서 `http://localhost:8000/` 주소로 접속하여 사이트를 확인합니다.

## 디렉터리 구조

- `common/` – 사용자 등록과 로그인 관련 뷰
- `pybo/` – Q&A 핵심 애플리케이션
- `templates/` – 장고 템플릿 파일
- `static/` – CSS·JavaScript 등 정적 파일
- `config/` – 프로젝트 설정 파일

## 테스트 실행

장고 기본 테스트 러너로 실행합니다.

```bash
python manage.py test
```

## 라이선스

이 프로젝트는 학습용 예제이며 별도의 라이선스를 포함하지 않습니다.
