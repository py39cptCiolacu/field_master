// Logout.js
import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

function Logout({ setIsAuthenticated, setUsername }) {
  const navigate = useNavigate();

  useEffect(() => {
    localStorage.removeItem('token');
    setIsAuthenticated(false);
    setUsername('');
    navigate('/login'); // Redirect to login page after logout
  }, [navigate, setIsAuthenticated, setUsername]);

  return (
    <div>
      <h2>Logging out...</h2>
    </div>
  );
}

export default Logout;
