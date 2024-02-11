import React, { useState, useEffect } from "react";
import MicRecorder from "mic-recorder-to-mp3";
import "./ClientComponent.css";
import WaveformComponent from "./WaveformComponent.js";

const Mp3Recorder = new MicRecorder({ bitRate: 128 });

const ClientComponent = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [blobURL, setBlobURL] = useState("");
  const [isBlocked, setIsBlocked] = useState(false);
  const [userLocation, setUserLocation] = useState(null);

  useEffect(() => {
    const getMicrophonePermissions = async () => {
      try {
        await navigator.mediaDevices.getUserMedia({ audio: true });
        setIsBlocked(false);
      } catch (error) {
        setIsBlocked(true);
        console.error("Permission Denied:", error);
      }
    };

    const getLocationPermissions = async () => {
      try {
        await navigator.geolocation.getCurrentPosition(async position => {
          const locationData = {
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
          };

          const response = await fetch(`https://maps.googleapis.com/maps/api/geocode/json?latlng=${locationData.latitude},${locationData.longitude}&key=${process.env.REACT_APP_GOOGLE_API_KEY}`);
          if (!response.ok) throw new Error('Failed to fetch address');
          const data = await response.json();
          locationData.address = data.results[0].formatted_address; 


          setUserLocation(locationData);
          console.log("User Location:", locationData);
          localStorage.setItem("userLocation", JSON.stringify(locationData));
        });
      } catch (error) {
        console.error("Location Permission Denied:", error);
      }
    };
    

    getMicrophonePermissions();
    getLocationPermissions();
  }, []);

  const startRecording = () => {
    if (isBlocked) {
      console.log("Permission Denied");
      return;
    }

    Mp3Recorder.start()
      .then(() => {
        setIsRecording(true);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  const stopRecording = () => {
    Mp3Recorder.stop()
      .getMp3()
      .then(([buffer, blob]) => {
        const audioUrl = URL.createObjectURL(blob);
        setBlobURL(audioUrl);
        setIsRecording(false);
        sendRecording(blob);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  const sendRecording = async (blob) => {
    try {
      const formData = new FormData();
      formData.append("audioFile", blob);

      const response = await fetch("http://127.0.0.1:5000/api/transcribe", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();

        console.log("Call ID:", data.callid);
      } else {
        console.error("Failed to transcribe audio");
      }
    } catch (error) {
      console.error("Error transcribing audio:", error);
    }
  };

  return (
    <div className="client-container">
      <h2 className="h2">
        <span style={{ fontFamily: 'monospace', fontWeight: 'bold' }}>Call.</span>
        <span style={{textDecoration: 'underline',fontFamily: 'monospace', color: 'red'}}><b>ER</b></span>
      </h2>

      <button
        className={`client-button record-button ${isRecording && "recording"}`}
        onClick={isRecording ? stopRecording : startRecording}
        disabled={isBlocked}
      >
        {isRecording ? (
          <svg
            width="800px"
            height="800px"
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              fillRule="evenodd"
              clipRule="evenodd"
              d="M14 7C15.6569 7 17 8.34315 17 10V14C17 15.6569 15.6569 17 14 17H10C8.34315 17 7 15.6569 7 14V10C7 8.34315 8.34315 7 10 7H14ZM14 9C14.5523 9 15 9.44772 15 10V14C15 14.5523 14.5523 15 14 15H10C9.44772 15 9 14.5523 9 14V10C9 9.44772 9.44772 9 10 9H14Z"
              fill="#0F0F0F"
            />
            <path
              fillRule="evenodd"
              clipRule="evenodd"
              d="M12 23C18.0751 23 23 18.0751 23 12C23 5.92487 18.0751 1 12 1C5.92487 1 1 5.92487 1 12C1 18.0751 5.92487 23 12 23ZM12 20.9932C7.03321 20.9932 3.00683 16.9668 3.00683 12C3.00683 7.03321 7.03321 3.00683 12 3.00683C16.9668 3.00683 20.9932 7.03321 20.9932 12C20.9932 16.9668 16.9668 20.9932 12 20.9932Z"
              fill="#0F0F0F"
            />
          </svg>
        ) : (
          <svg
            fill="#000000"
            height="800px"
            width="800px"
            version="1.1"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 512 512"
            xmlnsXlink="http://www.w3.org/1999/xlink"
          >
            <g>
              <g>
                <path d="m439.5,236c0-11.3-9.1-20.4-20.4-20.4s-20.4,9.1-20.4,20.4c0,70-64,126.9-142.7,126.9-78.7,0-142.7-56.9-142.7-126.9 0-11.3-9.1-20.4-20.4-20.4s-20.4,9.1-20.4,20.4c0,86.2 71.5,157.4 163.1,166.7v57.5h-23.6c-11.3,0-20.4,9.1-20.4,20.4 0,11.3 9.1,20.4 20.4,20.4h88c11.3,0 20.4-9.1 20.4-20.4 0-11.3-9.1-20.4-20.4-20.4h-23.6v-57.5c91.6-9.3 163.1-80.5 163.1-166.7z" />
                <path d="m256,323.5c51,0 92.3-41.3 92.3-92.3v-127.9c0-51-41.3-92.3-92.3-92.3s-92.3,41.3-92.3,92.3v127.9c0,51 41.3,92.3 92.3,92.3zm-52.3-220.2c0-28.8 23.5-52.3 52.3-52.3s52.3,23.5 52.3,52.3v127.9c0,28.8-23.5,52.3-52.3,52.3s-52.3-23.5-52.3-52.3v-127.9z" />
              </g>
            </g>
          </svg>
        )}
      </button>

      <WaveformComponent audioUrl={blobURL} />
      {/* <audio className="audio-player" src={blobURL} controls="controls" /> */}
  
      {userLocation && (
        <div className="location-container">
        <p style={{ fontFamily: 'monospace', fontWeight: 'bold' }}>Location Identified:</p>
        <p className="location-coordinates" style={{ fontFamily: 'monospace' }}>{userLocation.address}</p>
        <p className="location-coordinates" style={{ fontFamily: 'monospace' }}>({userLocation.latitude}, {userLocation.longitude})</p>
    </div>
      )}
    </div>
  );
};

export default ClientComponent;
