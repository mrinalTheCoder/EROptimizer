from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/api/transcribe', methods=['POST'])
def transcribe_audio():
    try:
        audio_file = request.files['audioFile']
        save_dir = request.form.get('saveDir', 'recordings')
        os.makedirs(save_dir, exist_ok=True)
        audio_path = os.path.join(save_dir, 'audio.mp3')
        audio_file.save(audio_path)
        
        # Invoke Whisper AI
        command = f'whisper "{audio_path}" --model medium.en'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        transcript = result.stdout.strip()
        
        # Save transcript to a text file in the same directory
        transcript_file = os.path.join(save_dir, 'transcript.txt')
        with open(transcript_file, 'w') as f:
            f.write(transcript)
        
        return jsonify({'transcript': transcript, 'transcript_file': transcript_file}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'Failed to transcribe audio'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)

