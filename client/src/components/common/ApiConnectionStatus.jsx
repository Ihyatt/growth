import React, { useState } from 'react';

function ApiConnectionStatus() {
  const [apiState, setApiState] = useState({
    message: '',
    error: null,
    loading: false,
    postResponse: null
  });
  
  const API_BASE_URL = 'http://localhost:5000/api';

  // Generic API caller function
  const callApi = async (endpoint, method = 'GET', body = null) => {
    setApiState(prev => ({ ...prev, loading: true, error: null }));
    
    try {
      const options = {
        method,
        headers: { 'Content-Type': 'application/json' },
      };
      
      if (body) options.body = JSON.stringify(body);
      
      const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
      
      if (!response.ok) {
        throw new Error(`API Error: ${response.status} ${response.statusText}`);
      }
      
      const data = await response.json();
      
      setApiState(prev => ({
        ...prev,
        loading: false,
        message: method === 'GET' ? data.message || data : null,
        postResponse: method === 'POST' ? data : null
      }));
      
      return data;
      
    } catch (error) {
      console.error(`${method} request failed:`, error);
      setApiState(prev => ({
        ...prev,
        loading: false,
        error: error.message
      }));
      throw error;
    }
  };

  // Specific API actions
  const fetchLuna = () => callApi('/luna');
  const fetchRomeo = () => callApi('/romeo');

  return (
    <div style={{ padding: '20px', maxWidth: '600px', margin: '0 auto' }}>
      <h1>API Connection Tester</h1>
      
      <div style={{ marginBottom: '20px' }}>
        <button 
          onClick={fetchLuna}
          disabled={apiState.loading}
          style={buttonStyle}
        >
          Luna
        </button>
        
        <button 
          onClick={fetchRomeo}
          disabled={apiState.loading}
          style={buttonStyle}
        >
          Romeo
        </button>
  
      </div>
      
      {apiState.loading && <p style={{ color: '#2196F3' }}>Loading...</p>}
      
      {apiState.error && (
        <div style={{ color: '#f44336', padding: '10px', border: '1px solid #f44336', borderRadius: '4px' }}>
          Error: {apiState.error}
        </div>
      )}
      
      {apiState.message && (
        <div style={{ marginTop: '20px', padding: '10px', backgroundColor: '#e8f5e9', borderRadius: '4px' }}>
          <h3>GET Response:</h3>
          <pre>{JSON.stringify(apiState.message, null, 2)}</pre>
        </div>
      )}
      
      {apiState.postResponse && (
        <div style={{ marginTop: '20px', padding: '10px', backgroundColor: '#e3f2fd', borderRadius: '4px' }}>
          <h3>POST Response:</h3>
          <pre>{JSON.stringify(apiState.postResponse, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

// Style object
const buttonStyle = {
  padding: '10px 15px',
  margin: '0 10px 10px 0',
  backgroundColor: '#2196F3',
  color: 'white',
  border: 'none',
  borderRadius: '4px',
  cursor: 'pointer',
  fontSize: '14px'
};

export default ApiConnectionStatus;