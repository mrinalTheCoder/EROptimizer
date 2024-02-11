// Waveform.js
import React, { useEffect, useRef } from 'react';
import WaveSurfer from 'wavesurfer.js';

const WaveformComponent = ({ audioUrl }) => {
  const waveformRef = useRef(null);
  const wavesurfer = useRef(null);

  useEffect(() => {
    wavesurfer.current = WaveSurfer.create({
      container: waveformRef.current,
      waveColor: "#00FFFF",
      progressColor: '#45a049',
      cursorColor: '#333',
      barWidth: 3,
      cursorWidth: 1,
      height: 100,
      responsive: true,
    });

    return () => {
      if (wavesurfer.current) {
        wavesurfer.current.destroy();
      }
    };
  }, []);

  useEffect(() => {
    if (audioUrl) {
      wavesurfer.current.load(audioUrl);

      // Start the playback if audio is loaded
      wavesurfer.current.play();
    }
  }, [audioUrl]);

  return <div ref={waveformRef} className="waveform" />;
};

export default WaveformComponent;
