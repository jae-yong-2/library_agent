# library_agent

# 시작하기

# backend 디렉토리로 이동

cd backend

# 가상환경이 있다면 활성화 (선택적)

source venv/bin/activate # Mac/Linux
venv\Scripts\activate # Windows

# 서버 실행

uvicorn main:app --reload --port 8000

# frontend 디렉토리로 이동

cd frontend

# 개발 서버 실행

npm run dev

브라우저에서 접속:
👉 http://localhost:5173 (React)
👉 http://localhost:8000/docs (FastAPI Swagger UI)
