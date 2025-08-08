import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Home from "./pages/Home";
import Books from "./pages/Books";
import "./App.css";

export default function App() {
  return (
    <div className="app">
      <Router>
        <header style={{ background:"#eee", padding:"10px 12px" }}>
          <nav style={{ display:"flex", gap:12 }}>
            <Link to="/">홈</Link>
            <Link to="/books">도서 목록</Link>
          </nav>
        </header>

        <main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/books" element={<Books />} />
          </Routes>
        </main>
      </Router>
    </div>
  );
}
