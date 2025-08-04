import { useState } from 'react'
import './App.css'

function App() {
  const [books, setBooks] = useState([]);
  const [message, setMessage] = useState("조회 전입니다.");

  const fetchBooks = () => {
    fetch("http://localhost:8000/api/books")
      .then(res => res.json())
      .then(data => {
        setMessage(data.message);
        setBooks(data.data);
      })
      .catch(err => {
        setMessage("에러 발생: " + err);
        setBooks([]);
      });
  };

  return (
    <div className="App">
      <h1>도서 정보 조회</h1>
      <button onClick={fetchBooks}>도서 목록 가져오기</button>
      <p>{message}</p>
      <table>
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
                <td key={i}>{val}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
