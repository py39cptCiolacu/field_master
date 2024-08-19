import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import './App.css';
import Login from './pages/Login/Login';
import Register from './pages/Register/Register';
import Map from './pages/Map/Map';
import UserProfile from './pages/UserProfile/UserProfile';
import Analysis from './pages/Analysis/Analysis';
import Logout from './pages/Logout/Logout';

import Navbar from './components/Navbar';
import Footer from './components/Footer';
import LandingPage from './components/LandingPage';


import 'mdb-react-ui-kit/dist/css/mdb.min.css';
import { Helmet } from 'react-helmet';

function App() {
  const [username, setUsername] = useState('');
  const [isAuthenticated, setIsAuthenticated] = useState(!!localStorage.getItem('token'));

  // Verificăm dacă există un token în localStorage și actualizăm starea
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      setUsername(username)// Într-un caz real, obține username-ul din token
      setIsAuthenticated(true);
    } else {
      setUsername('');
      setIsAuthenticated(false);
    }
  }, []);

  return (
    <Router>
      <div className="App">
        <Navbar isAuthenticated={isAuthenticated} username={username} />
        <Routes>
          <Route path="/login" element={<Login setUsername={setUsername} setIsAuthenticated={setIsAuthenticated} />} />
          <Route path="/register" element={<Register />} />
          <Route path="/" element={<Home />} />
          
          <Route path="/user_profile" element={
            <PrivateRoute>
              <UserProfile />
            </PrivateRoute>
          } />
          <Route path="/map" element={
            <PrivateRoute>
              <Map />
            </PrivateRoute>
          } />
          <Route path="/analysis" element={
            <PrivateRoute>
              <Analysis />
            </PrivateRoute>
          } />
          <Route path="/logout" element={
            <PrivateRoute>
              <Logout setIsAuthenticated={setIsAuthenticated} setUsername={setUsername} />
            </PrivateRoute>
          } />
        </Routes>
        <Footer />
      </div>
    </Router>
  );
}

// Componentă pentru rutele protejate
function PrivateRoute({ children }) {
  const token = localStorage.getItem('token');
  return token ? children : <Navigate to="/login" />;
}

function Home() {
  return (
    <div>
      <Helmet>
      <title>Home - FieldMaster</title>
      </Helmet>
      <LandingPage />
    </div>
  );
}

export default App;
