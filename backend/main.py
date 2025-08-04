import os
os.environ["TK_SILENCE_DEPRECATION"] = "1"

from datetime import date, datetime
import oracledb
import traceback
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# DB 설정
DB_USER = "system"
DB_PASSWORD = "pass"
DB_DSN = "localhost:1521/xe"
SCHEMA_OWNER = ""

app = FastAPI()

# CORS 설정 (React에서 API 호출 가능하도록)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite 기본 포트
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def format_date(value):
    if isinstance(value, (datetime, date)):
        return value.strftime("%Y-%m-%d")
    return value

@app.get("/api/books")
def fetch_books():
    table_ref = "BOOKS" if not SCHEMA_OWNER else f'{SCHEMA_OWNER}.BOOKS'
    sql = f"SELECT * FROM {table_ref}"

    try:
        conn = oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN)
        cursor = conn.cursor()

        cursor.execute(sql)
        desc = cursor.description
        if not desc:
            return {"message": "컬럼 정보를 불러오지 못했습니다.", "data": []}

        colnames = [d[0] for d in desc]
        rows = cursor.fetchall()
        formatted_rows = []

        for row in rows:
            formatted = [format_date(v) for v in row]
            row_dict = dict(zip(colnames, formatted))
            formatted_rows.append(row_dict)

        cursor.close()
        conn.close()

        return {"message": f"{len(rows)}건 조회됨", "data": formatted_rows}

    except oracledb.DatabaseError as e:
        return {"message": f"DB 오류: {str(e)}", "data": []}
    except Exception as e:
        return {"message": f"오류: {str(e)}", "data": []}
