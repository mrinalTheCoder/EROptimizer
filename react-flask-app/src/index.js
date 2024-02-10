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
        saveRecording(blob);
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  };

  const saveRecording = async (blob) => {
    // Specify the custom file name
    const fileName = 'recording.mp3';

    try {
        // Request access to the file system
        const fileHandle = await window.showSaveFilePicker();

        // Create a writable stream to the file
        const writable = await fileHandle.createWritable();

        // Write the blob data to the file
        await writable.write(blob);

        // Close the writable stream
        await writable.close();

        console.log('File saved successfully.');
    } catch (err) {
        console.error('Error saving file:', err);
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
