import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import './Login.css';
import {
  MDBBtn,
  MDBContainer,
  MDBRow,
  MDBCol,
  MDBCard,
  MDBCardBody,
  MDBInput
} from 'mdb-react-ui-kit';
import { Helmet } from 'react-helmet'; // Import Helmet

function Login({ setUsername, setIsAuthenticated }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      const response = await fetch('http://127.0.0.1:5000/api/v1/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (response.status === 200) {
        localStorage.setItem('token', data.access_token);
        setUsername(email);
        setIsAuthenticated(true);
        navigate('/user_profile');
      } else {
        setMessage(data.message);
      }
    } catch (error) {
      setMessage('An error occurred. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style = {{paddingTop: '50px', paddingBottom: '500px'}}>
      <Helmet>
        <title>Login - YourApp</title> {/* Set the page title */}
      </Helmet>
      <MDBContainer fluid className='p-4'>
        <MDBRow>
          <MDBCol md='6' className='text-center text-md-start d-flex flex-column justify-content-center'>
            <h1 className="my-5 display-3 fw-bold ls-tight px-3">
              The best offer <br />
              <span className="text-primary">for your business</span>
            </h1>
            <p className='px-3' style={{ color: 'hsl(217, 10%, 50.8%)' }}>
              Lorem ipsum dolor sit amet consectetur adipisicing elit.
              Eveniet, itaque accusantium odio, soluta, corrupti aliquam
              quibusdam tempora at cupiditate quis eum maiores libero
              veritatis? Dicta facilis sint aliquid ipsum atque?
            </p>
          </MDBCol>
          <MDBCol md='6'>
            <MDBCard className='my-5'>
              <MDBCardBody className='p-5'>
                <form onSubmit={handleLogin}>
                  <MDBInput
                    wrapperClass='mb-4'
                    label='Email'
                    id='form1'
                    type='email'
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                  />
                  <MDBInput
                    wrapperClass='mb-4'
                    label='Password'
                    id='form1'
                    type='password'
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                  />
                  <MDBBtn className='w-100 mb-4' size='md' type='submit' disabled={loading}>
                    {loading ? 'Logging in...' : 'Login'}
                  </MDBBtn>
                </form>
                {message && <p className="text-center">{message}</p>}
                <div className="text-center">
                  <p> Don't you have an account? <Link to="/register"> Register </Link></p>
                </div>
              </MDBCardBody>
            </MDBCard>
          </MDBCol>
        </MDBRow>
      </MDBContainer>
    </div>
  );
}

export default Login;
