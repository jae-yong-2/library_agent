import { Link } from "react-router-dom";

function Home() {
  return (
    <div style={{
      display: "flex",
      flexDirection: "column",
      justifyContent: "center",
      alignItems: "center",
      minHeight: "100vh",
      textAlign: "center"
    }}>
      <h1>홈 페이지</h1>
      <p>도서 정보를 확인하려면 아래 버튼을 클릭하세요.</p>
      <Link to="/books">
        <button>도서 목록 페이지로 이동</button>
      </Link>
    </div>
  );
}

export default Home;
