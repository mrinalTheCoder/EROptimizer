import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import MicRecorder from 'mic-recorder-to-mp3';

const Mp3Recorder = new MicRecorder({ bitRate: 128 });

const Index = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [blobURL, setBlobURL] = useState('');
  const [isBlocked, setIsBlocked] = useState(false);

  useEffect(() => {
    const getMicrophonePermissions = async () => {
      try {
        await navigator.mediaDevices.getUserMedia({ audio: true });
        setIsBlocked(false);
      } catch (error) {
        setIsBlocked(true);
        console.error('Permission Denied:', error);
      }
    };

    getMicrophonePermissions();
  }, []);

  const startRecording = () => {
    if (isBlocked) {
      console.log('Permission Denied');
      return;
    }

    Mp3Recorder.start()
      .then(() => {
        setIsRecording(true);
      })
      .catch((error) => {
        console.error('Error:', error);
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
        console.error('Error:', error);
      });
  };

  const sendRecording = async (blob) => {
    try {
      const formData = new FormData();
      formData.append('audioFile', blob);

      const response = await fetch('http://127.0.0.1:5000/api/transcribe', {
        method: 'POST',
        body: formData
      });

      if (response.ok) {
        const data = await response.json();
        console.log('Transcription:', data.transcript);
      } else {
        console.error('Failed to transcribe audio');
      }
    } catch (error) {
      console.error('Error transcribing audio:', error);
    }
  };

  return (
    <React.StrictMode>
      <App />
      <button onClick={startRecording} disabled={isRecording || isBlocked}>
        Record
      </button>
      <button onClick={stopRecording} disabled={!isRecording}>
        Stop
      </button>
      <audio src={blobURL} controls="controls" />
    </React.StrictMode>
  );
};

ReactDOM.render(<Index />, document.getElementById('root'));
