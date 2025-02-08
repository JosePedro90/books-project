import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Login from "./pages/Login";

import BookListPage from "./pages/BookListPage";
import ProtectedRoute from "./components/ProtectedRoute";
import BookDetailsPage from "./pages/BookDetailsPage";

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<BookListPage />} />
        <Route path="/login" element={<Login />} />
        <Route
          path="/books/:id"
          element={
            <ProtectedRoute>
              <BookDetailsPage />
            </ProtectedRoute>
          }
        />
      </Routes>
    </Router>
  );
};

export default App;
