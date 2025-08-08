import { useState, useEffect } from "react";

function Books() {
  const [books, setBooks] = useState([]);
  const [message, setMessage] = useState("조회 중입니다...");
  const [loading, setLoading] = useState(false);

  const fetchBooks = () => {
    setLoading(true);
    fetch("http://localhost:8000/api/books")
      .then(res => res.json())
      .then(data => {
        setMessage(data.message);
        setBooks(data.data);
      })
      .catch(err => {
        setMessage("에러 발생: " + err);
        setBooks([]);
      })
      .finally(() => setLoading(false));
  };

  const resetDummy = () => {
    if (!confirm("정말 테이블을 리셋하고 더미 30개를 삽입할까요?")) return;
    setLoading(true);
    fetch("http://localhost:8000/api/books/reset", {
      method: "POST",
    })
      .then(res => res.json())
      .then(data => {
        setMessage(data.message || "리셋 완료");
        // 리셋 후 목록 다시 로드
        fetchBooks();
      })
      .catch(err => {
        setMessage("리셋 중 에러 발생: " + err);
      })
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchBooks();
  }, []);

  return (
    <div style={{
      display: "flex",
      flexDirection: "column",
      justifyContent: "center",
      alignItems: "center",
      minHeight: "100vh",
      textAlign: "center"
    }}>
      <h1>도서 정보 조회</h1>

      <div style={{ display: "flex", gap: 8, marginBottom: 12 }}>
        <button onClick={fetchBooks} disabled={loading}>
          새로고침
        </button>
        <button onClick={resetDummy} disabled={loading} style={{ background: "#ffd966" }}>
          더미 데이터 리셋
        </button>
      </div>

      <p>{loading ? "로딩 중..." : message}</p>

      <div style={{
        display: "flex",
        justifyContent: "center",
        width: "100%",
        overflowX: "auto"
      }}>
        <table border="1" cellPadding="5" style={{ marginTop: "20px" }}>
          <thead>
            <tr>
              {books.length > 0 &&
                Object.keys(books[0]).map((col) => <th key={col}>{col}</th>)}
            </tr>
          </thead>
          <tbody>
            {books.map((book, idx) => (
              <tr key={idx}>
                {Object.values(book).map((val, i) => (
                  <td key={i}>{String(val)}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Books;
