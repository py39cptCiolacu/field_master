import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './UserProfile.css';
import {
  MDBCol, MDBContainer, MDBRow, MDBCard, MDBCardText, MDBCardBody, 
  MDBCardImage, MDBBtn, MDBTypography, MDBTable, MDBTableHead, MDBTableBody, MDBModal, MDBModalHeader, MDBModalBody, MDBModalFooter
} from 'mdb-react-ui-kit';
import { Helmet } from 'react-helmet';

function UserProfile() {
  const [userInfo, setUserInfo] = useState(null);
  const [error, setError] = useState(null);
  const [modalOpen, setModalOpen] = useState(false); // State for modal
  const [newUsername, setNewUsername] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUserInfo = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch('http://127.0.0.1:5000/api/v1/user_profile', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        });

        if (response.status === 401) {
          navigate('/login');
          return;
        }

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.message || 'Something went wrong');
        }

        setUserInfo(data);
        setNewUsername(data.username); // Initialize newUsername with current username
      } catch (error) {
        console.error('Fetch error:', error);
        setError(error.message);
      }
    };

    fetchUserInfo();
  }, [navigate]);

  const handleEditProfile = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://127.0.0.1:5000/api/v1/update_username', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ newUsername })
      });

      if (!response.ok) {
        throw new Error('Failed to update username');
      }

      const data = await response.json();
      setUserInfo((prevInfo) => ({ ...prevInfo, username: newUsername }));
      setModalOpen(false);
    } catch (error) {
      console.error('Update error:', error);
      setError(error.message);
    }
  };

  if (error) {
    return <div className="user-profile-container"><p>{error}</p></div>;
  }

  return (
    <div className="gradient-custom-2" style={{paddingTop: '20px'}}>
      <Helmet>
        <title>User Profile - FieldMaster</title>
      </Helmet>
      <MDBContainer className="py-5 h-100 w-10">
        <MDBRow className="justify-content-center align-items-center h-100">
          <MDBCol lg="9" xl="7">
            <MDBCard>
              <div className="rounded-top text-white d-flex flex-row" style={{ backgroundColor: '#000', height: '200px' }}>
                <div className="ms-4 mt-5 d-flex flex-column" style={{ width: '150px' }}>
                  <MDBCardImage 
                    src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-profiles/avatar-1.webp"
                    alt="Generic placeholder image" 
                    className="mt-4 mb-2 img-thumbnail" 
                    fluid 
                    style={{ width: '200px', zIndex: '1' }} 
                  />
                </div>
                <div className="ms-3" style={{ marginTop: '130px' }}>
                  {userInfo ? (
                    <>
                      <MDBTypography tag="h5">{userInfo.username}</MDBTypography>
                      <MDBCardText>{userInfo.email}</MDBCardText>
                    </>
                  ) : (
                    <MDBCardText>Loading...</MDBCardText>
                  )}
                </div>
              </div>
              <div className="p-4 text-black" style={{ backgroundColor: '#f8f9fa' }}>
                <div className="d-flex justify-content-end text-center py-1">
                  <div>
                    <MDBCardText className="mb-1 h3">{userInfo?.number_of_lands}</MDBCardText>
                    <MDBCardText className="small text-muted mb-0">Lands</MDBCardText>
                  </div>
                  <div className="px-3">
                    <MDBCardText className="mb-1 h3">30</MDBCardText>
                    <MDBCardText className="small text-muted mb-0">Suggestions</MDBCardText>
                  </div>
                </div>
              </div>
              <MDBCardBody className="text-black p-4">
                <div className="mb-5">
                  <p className="lead fw-normal mb-1" style={{paddingBottom: '20px'}}>Functionalities</p>
                  <div className="row">
                    <div className="col-md-6 d-flex justify-content-center align-items-center" style={{ height: '200px' }}>
                      <div className="d-flex flex-column align-items-center">
                        <MDBBtn className="mb-3" style={{ backgroundColor: '#00b300', width: '150px' }} onClick={() => navigate('/map')}>Add Land</MDBBtn>
                        <MDBBtn className="mb-3" style={{ backgroundColor: '#00b300', width: '150px' }} onClick={() => navigate('/analysis')}>Get Analysis</MDBBtn>
                        <MDBBtn style={{ backgroundColor: '#00b300', width: '150px' }} onClick={() => setModalOpen(true)}>Edit profile</MDBBtn>
                      </div>
                    </div>
                    <div className="col-md-6">
                      <div className="border rounded p-3" style={{ backgroundColor: '#f8f9fa' }}>
                        <h5 className="fw-bold text-center mb-2">Your last suggestion</h5>
                        <p className="text-muted mb-0" style={{ fontSize: '0.875rem', textAlign: 'justify' }}>
                          Here you can find functionalities to manage your lands. Use the buttons on the left to add new lands, get analysis, or perform other actions. Make sure to explore all available options to fully utilize the platform.
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
                <div className="d-flex justify-content-between align-items-center mb-4">
                  <MDBCardText className="lead fw-normal mb-0">Lands</MDBCardText>
                </div>
                <MDBTable>
                  <MDBTableHead>
                    <tr>
                      <th>ID</th>
                      <th>Name</th>
                      <th>Size</th>
                    </tr>
                  </MDBTableHead>
                  <MDBTableBody>
                    {userInfo && userInfo.lands.length > 0 ? (
                      userInfo.lands.map((land) => (
                        <tr key={land.id}>
                          <td>{land.id}</td>
                          <td>{land.name}</td>
                          <td>{land.size}</td>
                        </tr>
                      ))
                    ) : (
                      <tr>
                        <td colSpan="3">No lands available</td>
                      </tr>
                    )}
                  </MDBTableBody>
                </MDBTable>
              </MDBCardBody>
            </MDBCard>
          </MDBCol>
        </MDBRow>
      </MDBContainer>

      {/* Modal for editing profile */}
      <MDBModal show={modalOpen} setShow={setModalOpen} tabIndex='-1'>
        <MDBModalHeader>Update Username</MDBModalHeader>
        <MDBModalBody>
          <div className="form-outline">
            <input
              type="text"
              className="form-control"
              value={newUsername}
              onChange={(e) => setNewUsername(e.target.value)}
            />
          </div>
        </MDBModalBody>
        <MDBModalFooter>
          <MDBBtn color="secondary" onClick={() => setModalOpen(false)}>Close</MDBBtn>
          <MDBBtn onClick={handleEditProfile} style={{ backgroundColor: '#00b300' }}>Save Changes</MDBBtn>
        </MDBModalFooter>
      </MDBModal>
    </div>
  );
}

export default UserProfile;
