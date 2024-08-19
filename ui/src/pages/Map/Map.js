import React, { useState } from 'react';
import axios from 'axios';
import { MapContainer, TileLayer, Marker, Polygon, useMapEvents } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { MDBBtn, MDBInput } from 'mdb-react-ui-kit';
import 'mdb-react-ui-kit/dist/css/mdb.min.css'; // Import MDB CSS
import { Helmet } from 'react-helmet'; // Import Helmet

// Fix the marker icon issue by using the default Leaflet icon
delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

const MapClickHandler = ({ setPoints, setPolygon, points }) => {
  useMapEvents({
    click: (e) => {
      const newPoint = [e.latlng.lat, e.latlng.lng];
      let newPoints = [...points, newPoint];

      if (newPoints.length === 5) {
        newPoints = [newPoint];  // Reset to the new point only
      }

      setPoints(newPoints);

      if (newPoints.length === 4) {
        setPolygon(newPoints);
      } else {
        setPolygon(null);
      }

      axios.post('http://localhost:5000/api/v1/get_coordinates', { lat: e.latlng.lat, lng: e.latlng.lng })
        .then(response => {
          console.log('Server response:', response.data);
        })
        .catch(error => console.error('Error posting coordinates:', error));
    }
  });

  return null;
};

const MapComponent = () => {
  const [points, setPoints] = useState([]);
  const [polygon, setPolygon] = useState(null);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [landName, setLandName] = useState(''); // State for the land name

  const handleAddLand = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No authentication token found');
      }

      if (points.length === 4 && landName.trim()) {
        const response = await axios.post(
          'http://localhost:5000/api/v1/add_land',
          { points, name: landName }, // Include land name in the request body
          {
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
            }
          }
        );

        console.log('Server response:', response.data);
        setPoints([]);  // Optionally clear the points after successful submission
        setPolygon(null);
        setLandName(''); // Clear the land name input
        setSuccess('Land added successfully!');
        setError(null);
      } else {
        setError('You must select exactly 4 points and provide a land name.');
        setSuccess(null);
      }
    } catch (error) {
      console.error('Error adding land:', error.response ? error.response.data : error.message);
      // Display the error message from the backend
      setError(error.response ? error.response.data.message : error.message);
      setSuccess(null);
    }
  };

  const handleDeletePoints = () => {
    setPoints([]);
    setPolygon(null);
    setError(null); // Clear error messages
    setSuccess(null); // Clear success messages
    setLandName(''); // Clear land name input
  };

  return (
    <div style={{ display: 'flex', alignItems: 'center', paddingTop: '70px' }}>
      <Helmet>
        <title>Add Land - FieldMaster</title> {/* Set the page title */}
      </Helmet>
      <div style={{ 
        flex: 1, 
        position: 'relative',
        borderRadius: '10px',
        overflow: 'hidden',
        marginRight: '10px'
      }}>
        <MapContainer 
          center={[0, 0]} 
          zoom={2} 
          style={{ 
            height: '500px', 
            width: 'calc(100% - 20px)'  
          }}
        >
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          <MapClickHandler 
            setPoints={setPoints} 
            setPolygon={setPolygon} 
            points={points} 
          />
          {points.map((point, index) => (
            <Marker key={index} position={point} />
          ))}
          {polygon && <Polygon positions={polygon} color="red" />}
        </MapContainer>
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', alignItems: 'center' }}>
        <MDBInput
          label="Land Name"
          value={landName}
          onChange={(e) => setLandName(e.target.value)}
          style={{ width: '200px', marginBottom: '10px' }}
        />
        <MDBBtn 
          style={{ backgroundColor: '#00b300', width: '120px' }} 
          onClick={handleAddLand}
        >
          Add Land
        </MDBBtn>
        <MDBBtn 
          style={{ backgroundColor: '#00b300', width: '120px' }} 
          onClick={handleDeletePoints}
        >
          Delete
        </MDBBtn>
        {success && <div style={{ color: 'green', marginTop: '10px' }}>{success}</div>}
        {error && <div style={{ color: 'red', marginTop: '10px' }}>{error}</div>}
      </div>
    </div>
  );
};

export default MapComponent;
