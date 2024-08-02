import React, { useState } from 'react';
import { useNavigate  } from 'react-router-dom';
import './signin.css';
import axios from 'axios';

function SignIn() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const navigate = useNavigate();

    const handleSignIn = async () => {
        try {
          const response = await axios.post('http://127.0.0.1:5000/signin', {
            user: username,
            pass: password
          });
    
          if (response.data === "success") {
            navigate('/dashboard');
          }
        } catch (error) {
          if (error.response) {
            setError(error.response.data.message);
          } else {
            setError('An error occurred. Please try again.');
          }
        }
      };
  return (
    <div className="signin-container">
      <h2>Sign In</h2>
      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button onClick={handleSignIn}>Sign In</button>
      {error && <p>{error}</p>}
    </div>
  );
}

export default SignIn;
