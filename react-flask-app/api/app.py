from flask import Flask, request, jsonify
import subprocess
import os
from flask_cors import CORS


app = Flask(__name__)
CORS(app)



@app.route('/api/transcribe', methods=['POST'])
def transcribe_audio():
    try:
        os.makedirs("whisper_out", exist_ok=True)
        os.chdir("whisper_out")


        audio_file = request.files['audioFile']
        subdir = request.form['audioName']

        os.makedirs(subdir, exist_ok=True)
        os.chdir(subdir)

        
        

        audio_file.save("audio.mp3")
        
        # Invoke Whisper AI 
        # We should consider using command more similar to this: https://github.com/openai/whisper#python-usage
       
        command = f'whisper ./audio.mp3 --model medium.en'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        transcript = result.stdout.strip()
        
        # Save transcript to a text file in the same directory
        transcript_file = os.path.join('transcript.txt')
        with open(transcript_file, 'w') as f:
            f.write(transcript)
        
        os.chdir("../..")
        
        return jsonify({'transcript': transcript}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'Failed to transcribe audio'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

