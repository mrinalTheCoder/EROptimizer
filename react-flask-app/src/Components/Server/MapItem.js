import React, { useEffect, useRef, useState } from 'react';

const MapItem = () => {
  const mapRef = useRef(null);
  const storedLocation = JSON.parse(localStorage.getItem('userLocation'));
  const [transportationTime, setTransportationTime] = useState(null);
  const GOOGLE_API_KEY = process.env.REACT_APP_GOOGLE_API_KEY

  useEffect(() => {
    const script = document.createElement('script');
    script.src = `https://maps.googleapis.com/maps/api/js?key=` + GOOGLE_API_KEY + `&libraries=places&callback=initMap`;
    script.async = true;
    script.defer = true;
    document.body.appendChild(script);

    return () => {
      document.body.removeChild(script);
    };
  }, []);

  window.initMap = () => {
    if (storedLocation) {
      const mapOptions = {
        zoom: 13,
        center: { lat: storedLocation.latitude, lng: storedLocation.longitude },
      };

      const map = new window.google.maps.Map(mapRef.current, mapOptions);

      // Marker for stored location
      const storedLocationMarker = new window.google.maps.Marker({
        position: { lat: storedLocation.latitude, lng: storedLocation.longitude },
        map: map,
        icon: 'https://maps.google.com/mapfiles/ms/icons/blue-dot.png',
      });

      const hardcodedLocation = { lat: 33.7914, lng: -84.3195 };

      // Marker for hardcoded destination
      const hardcodedDestinationMarker = new window.google.maps.Marker({
        position: hardcodedLocation,
        map: map,
        icon: 'https://maps.google.com/mapfiles/ms/icons/red-dot.png',
      });

      // Calculate distance and time using Distance Matrix API
      const service = new window.google.maps.DistanceMatrixService();
      const origin = new window.google.maps.LatLng(storedLocation.latitude, storedLocation.longitude);
      const destination = new window.google.maps.LatLng(hardcodedLocation.lat, hardcodedLocation.lng);
      const request = {
        origins: [origin],
        destinations: [destination],
        travelMode: window.google.maps.TravelMode.DRIVING,
      };
      service.getDistanceMatrix(request, (response, status) => {
        if (status === 'OK') {
          const duration = response.rows[0].elements[0].duration.text;
          setTransportationTime(duration);
        } else {
          console.error('Distance Matrix request failed:', status);
        }
      });
    }
  };

  return (
    <div className="map-container" style={{ width: '100%', height: '100px' }}>
      <div ref={mapRef} style={{ width: '100%', height: '80%' }} />
        <div className="location-container">
          <p style={{ fontFamily: 'monospace', fontWeight: 'bold' }}>Time to arrival: {transportationTime}</p>
         </div>
    </div>
  );  
};

export default MapItem;
