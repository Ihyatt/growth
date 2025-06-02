import React, { useEffect, useState } from 'react';
import { getToken, removeToken } from '../utils/auth';
import { useNavigate } from 'react-router-dom';

export default function Dashboard() {
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProtected = async () => {
      const token = getToken();
      const res = await fetch(`${import.meta.env.VITE_API_URL}/protected`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (!res.ok) {
        removeToken();
        navigate('/');
      } else {
        const data = await res.json();
        setMessage(data.message);
      }
    };
    fetchProtected();
  }, []);

  return (
    <div>
      <h1>Dashboard</h1>
      <p>{message}</p>
      <button onClick={() => { removeToken(); navigate('/'); }}>Logout</button>
    </div>
  );
}