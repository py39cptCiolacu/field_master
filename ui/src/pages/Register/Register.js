import React, { useState } from 'react';
import './Register.css';
import { Link } from 'react-router-dom'
import { Helmet } from 'react-helmet'
import {
  MDBBtn,
  MDBContainer,
  MDBRow,
  MDBCol,
  MDBCard,
  MDBCardBody,
  MDBInput,
  MDBCheckbox,
  MDBIcon
}
from 'mdb-react-ui-kit';

function Register() {
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [passwordConfirm, setPasswordConfirm] = useState('');
  const [message, setMessage] = useState('');

  const handleRegister = async (e) => {
    e.preventDefault();
    
    const response = await fetch('http://127.0.0.1:5000/api/v1/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, username, password, password_confirm: passwordConfirm }),
    });

    const data = await response.json();

    if (response.status === 201) {
      setMessage(data.message);
    } else {
      setMessage(data.message);
    }
  };

return (
  <div style = {{paddingTop: '50px', paddingBottom: '500px'}}>
  <MDBContainer fluid className='p-4'>
      <Helmet>
        <title>Register - FieldMaster</title>
      </Helmet>
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
            <form onSubmit={handleRegister}>
              <MDBRow>
                <MDBCol col='6'>
                  <MDBInput
                    wrapperClass='mb-4'
                    label='Username'
                    id='form1'
                    type='text'
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                  />
                </MDBCol>
                <MDBCol col='6'>
                  <MDBInput
                    wrapperClass='mb-4'
                    label='Email'
                    id='form1'
                    type='email'
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                  />
                </MDBCol>
              </MDBRow>
              <MDBInput
                wrapperClass='mb-4'
                label='Password'
                id='form2'
                type='password'
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
              <MDBInput
                wrapperClass='mb-4'
                label='Confirm Password'
                id='form3'
                type='password'
                value={passwordConfirm}
                onChange={(e) => setPasswordConfirm(e.target.value)}
                required
              />
              <MDBBtn className='w-100 mb-4' size='md' type='submit'>
                Register
              </MDBBtn>
            </form>
            {message && <p className="text-center">{message}</p>}
            <div className="text-center">
              <p>
                Already have an account? <Link to="/login">Login</Link>
              </p>
            </div>
          </MDBCardBody>
        </MDBCard>
      </MDBCol>
    </MDBRow>
  </MDBContainer>
  </div>
);
};

export default Register;
