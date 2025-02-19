import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import Index from './pages/Index';

const App: React.FC = () => {
  const isLoggedIn = !!localStorage.getItem('token'); // Check if user is logged in

  return (
    <BrowserRouter>
      <Routes>
        {/* Redirect to login if not logged in */}
        <Route
          path="/"
          element={isLoggedIn ? <Index /> : <Navigate to="/login" />}
        />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/main" element={<Index />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;