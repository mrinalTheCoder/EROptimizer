from flask import Flask, request, jsonify
import subprocess
import os
from flask_cors import CORS
from flask_cors import cross_origin
import json

app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})


@app.route('/api/transcribe', methods=['POST'])
@cross_origin()
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
        #load transcript from audio.txt
        with open("audio.txt", "r") as file:
            transcript = file.read()

        transcript = transcript.replace("\n", " ")
        transcript = transcript.replace("\r", " ")
        transcript = transcript.replace("\t", " ")

        print("Transcript:", transcript)

        #write the callid and transcript to a json
        with open("transcript.json", "w") as file:
            file.write('{"callid": ' + '"' + subdir + '"' + ', "transcript": ' + '"' + transcript + '"' + '}')

        os.chdir("../..")
        



        return jsonify({'transcript': transcript}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'Failed to transcribe audio'}), 500
    
@app.route('/api/list_transcripts', methods=['GET'])
@cross_origin()
def list_transcripts():
    try:
        base_dir = "whisper_out"
        callids = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
        transcripts = []

        for callid in callids:
            transcript_path = os.path.join(base_dir, callid, "transcript.json")
            if os.path.exists(transcript_path):
                try:
                    with open(transcript_path, "r") as file:
                        transcript_data = json.load(file)  # Parses the JSON data
                        transcripts.append({"callid": callid, "data": transcript_data})
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from {transcript_path}")

        return jsonify(transcripts), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'Failed to list transcripts'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

