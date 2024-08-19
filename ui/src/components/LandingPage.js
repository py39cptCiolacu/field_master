import React from 'react';
import { MDBContainer, MDBRow, MDBCol, MDBBtn, MDBCard, MDBCardBody, MDBCardTitle, MDBCardText } from 'mdb-react-ui-kit';
import './LandingPage.css'

export default function LandingPage() {
  return (
    <MDBContainer fluid className="px-4 py-5 my-5 text-center background-image">
      <MDBRow className="align-items-center g-lg-5 py-5">
        <MDBCol lg="7" className="text-lg-start">
          <h1 className="display-4 fw-bold lh-1 mb-3">AI-Powered Agricultural Insights</h1>
          <p className="col-lg-10 fs-7">
          Harness the power of AI and satellite technology to transform your farming practices. 
          Get personalized recommendations, monitor crop health, and make data-driven decisions to boost productivity and profitability.
          </p>
          <MDBBtn rounded size="lg" style = {{backgroundColor:'#00b300'}}>Register Now </MDBBtn>

        </MDBCol>
        <MDBCol md="10" lg="5">
          <img src="/path-to-your-image.jpg" className="img-fluid" alt="Agriculture Image" />
        </MDBCol>
      </MDBRow>
      {/* <MDBRow className="mt-5">
        <MDBCol md="6" lg="4" className="mx-auto">
          <MDBCard className="text-center">
            <MDBCardBody>
              <MDBCardTitle className="text-primary">Our Services</MDBCardTitle>
              <MDBCardText>
                Discover the range of services we offer to enhance your farming practices. From advanced analytics to tailored recommendations, we are here to support you every step of the way.
              </MDBCardText>
              <MDBBtn href="#" color="primary">Learn More</MDBBtn>
            </MDBCardBody>
          </MDBCard>
        </MDBCol>
      </MDBRow> */}

    </MDBContainer>
  );
}
