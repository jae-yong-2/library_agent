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


@app.post("/api/books/reset")
def reset_books():
    table_ref = "BOOKS" if not SCHEMA_OWNER else f'{SCHEMA_OWNER}.BOOKS'

    try:
        conn = oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN)
        cursor = conn.cursor()

        # 1) BOOKS 테이블 데이터 삭제
        cursor.execute(f"DELETE FROM {table_ref}")

        # 2) 더미 데이터 30개 준비
        rows = [
            (1, '시간의 연대기', '김하늘', '미래출판사', datetime(2019, 3, 15), '대출가능',
            '시간 여행의 비밀을 알게 된 주인공이 과거와 미래를 넘나들며 역사의 중요한 순간에 개입하는 이야기.'),
            (2, '바다 건너편 이야기', '이서준', '파도출판', datetime(2020, 7, 21), '대출가능',
            '머나먼 섬마을에서 벌어지는 미스터리와 전설 속 괴생물의 실체를 추적하는 이야기.'),
            (3, '하늘 아래 첫 사랑', '박지민', '푸른책방', datetime(2018, 11, 3), '대출가능',
            '소년과 소녀가 계절의 변화 속에서 사랑을 키워가는 감동적인 이야기.'),
            (4, '빛과 그림자', '최민호', '빛의서재', datetime(2021, 5, 9), '대출가능',
            '도시의 어두운 이면과 그 속에서 피어나는 희망을 담은 감성 드라마.'),
            (5, '숲속의 비밀', '정유진', '초록출판사', datetime(2017, 8, 19), '대출가능',
            '깊은 숲 속에 숨겨진 마을과 그곳에서 전해 내려오는 신비한 전설을 탐험하는 이야기.'),
            (6, '달빛 아래 춤을', '윤서현', '달의서재', datetime(2019, 12, 25), '대출가능',
            '달빛이 가득한 밤, 춤을 통해 서로의 마음을 이해하게 되는 두 사람의 이야기.'),
            (7, '시간을 훔친 아이', '한지후', '시계출판', datetime(2022, 2, 10), '대출가능',
            '시간을 조작할 수 있는 힘을 가진 아이의 모험과 성장 이야기.'),
            (8, '잃어버린 왕국', '서아린', '황금출판사', datetime(2020, 10, 5), '대출가능',
            '사라진 왕국을 되찾기 위한 전사의 여정과 그 속에 숨겨진 음모.'),
            (9, '눈물의 바다', '김도현', '하늘바다', datetime(2018, 4, 14), '대출가능',
            '사랑하는 이를 잃은 주인공이 바다에서 새로운 삶의 의미를 찾는 이야기.'),
            (10, '사막의 노래', '박소연', '모래출판사', datetime(2019, 6, 30), '대출가능',
            '광활한 사막에서 전해 내려오는 고대의 노래와 숨겨진 보물을 찾아가는 여정.'),
            (11, '별빛 속으로', '정하늘', '우주서적', datetime(2021, 1, 18), '대출가능',
            '별빛을 따라 우주 여행을 떠나는 소년의 모험담.'),
            (12, '그림자의 추격자', '이민재', '스릴출판', datetime(2020, 9, 8), '대출가능',
            '도시 속 연쇄 사건의 배후를 쫓는 그림자 같은 형사의 이야기.'),
            (13, '푸른 강을 건너', '최서영', '물결출판', datetime(2018, 3, 22), '대출가능',
            '강 건너 마을에서 벌어지는 미스터리 사건을 풀어가는 소녀의 이야기.'),
            (14, '불꽃의 춤', '백승우', '열정서재', datetime(2019, 11, 11), '대출가능',
            '춤을 통해 세상의 불의를 마주하고 극복하는 이야기.'),
            (15, '마지막 편지', '김은지', '감성출판', datetime(2017, 5, 27), '대출가능',
            '사랑하는 이에게 남긴 마지막 편지에 얽힌 비밀을 찾아가는 여정.'),
            (16, '하얀 눈의 약속', '윤지호', '겨울출판사', datetime(2021, 12, 1), '대출가능',
            '눈 덮인 마을에서 다시 만난 첫사랑과의 약속을 지켜가는 이야기.'),
            (17, '검은 바람', '박재현', '바람서재', datetime(2020, 4, 6), '대출가능',
            '도시를 뒤덮은 검은 바람의 정체를 밝히기 위한 모험담.'),
            (18, '숨겨진 계곡', '이수빈', '자연출판사', datetime(2019, 8, 12), '대출가능',
            '지도에 표시되지 않은 계곡에서 벌어지는 신비한 사건들.'),
            (19, '별의 노래', '정민수', '하늘출판사', datetime(2018, 6, 2), '대출가능',
            '별이 들려주는 노래를 따라가며 잃어버린 추억을 찾는 이야기.'),
            (20, '기억의 숲', '최윤아', '기억서적', datetime(2022, 3, 14), '대출가능',
            '기억을 잃은 채 숲에서 깨어난 주인공의 정체를 찾아가는 여정.'),
            (21, '달의 그림자', '한서준', '달빛출판사', datetime(2020, 1, 7), '대출가능',
            '달빛 아래 나타나는 그림자의 비밀을 파헤치는 이야기.'),
            (22, '고요한 파도', '김다인', '바다서재', datetime(2019, 9, 18), '대출가능',
            '고요한 파도 속에 숨겨진 진실을 찾아 떠나는 항해기.'),
            (23, '사라진 아이', '박현우', '미스터리출판', datetime(2018, 2, 5), '대출가능',
            '도시 한복판에서 흔적 없이 사라진 아이를 찾는 이야기.'),
            (24, '불멸의 사랑', '윤채린', '영원출판사', datetime(2021, 7, 23), '대출가능',
            '세기를 넘어 이어지는 사랑과 그 속에 숨겨진 비밀.'),
            (25, '그날의 약속', '이도현', '추억서재', datetime(2020, 11, 17), '대출가능',
            '과거의 약속을 지키기 위해 현재를 바꾸는 이야기.'),
            (26, '푸른 달빛', '정우성', '달서적', datetime(2019, 4, 9), '대출가능',
            '푸른 달빛 아래에서 시작된 운명적인 만남.'),
            (27, '깊은 밤의 속삭임', '서지현', '밤출판사', datetime(2018, 10, 28), '대출가능',
            '깊은 밤에만 들을 수 있는 속삭임의 정체를 찾아가는 이야기.'),
            (28, '황금의 도시', '박찬호', '황금서재', datetime(2022, 5, 5), '대출가능',
            '전설 속 황금 도시를 찾기 위한 모험과 그 과정에서 벌어지는 사건들.'),
            (29, '시간의 문', '김태윤', '시계서적', datetime(2020, 6, 14), '대출가능',
            '시간의 문을 열고 과거와 미래를 넘나드는 여행자의 이야기.'),
            (30, '영원의 불꽃', '이하늘', '영원출판', datetime(2019, 8, 30), '대출가능',
            '영원히 꺼지지 않는 불꽃을 찾기 위해 떠나는 대서사시.')
        ]


        # 3) BOOKS 테이블에 데이터 삽입
        cursor.executemany(
            f"""
            INSERT INTO {table_ref}
            (BOOK_ID, TITLE, AUTHOR, PUBLISHER, PUBLISHED_DATE, STATUS, CONTENT)
            VALUES (:1, :2, :3, :4, :5, :6, :7)
            """,
            rows
        )

        conn.commit()
        cursor.close()
        conn.close()

        return {"message": f"테이블 리셋 완료: {len(rows)}건 삽입됨"}

    except oracledb.DatabaseError as e:
        return {"message": f"DB 오류: {str(e)}"}
    except Exception as e:
        return {"message": f"오류: {str(e)}"}
