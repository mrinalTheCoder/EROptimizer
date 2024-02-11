from flask import Flask, request, jsonify
import subprocess
import os
from flask_cors import CORS
from flask_cors import cross_origin
import json
import transcript_parser

app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})


@app.route('/api/transcribe', methods=['POST'])
@cross_origin()
def transcribe_audio():
    try:
        base_dir = "whisper_out"
        os.makedirs(base_dir, exist_ok=True)

        num_dirs = sum(os.path.isdir(os.path.join(base_dir, d)) for d in os.listdir(base_dir))
        subdir = f"Call-{num_dirs:02}"
        subdir_path = os.path.join(base_dir, subdir)
        os.makedirs(subdir_path, exist_ok=True)
        

        audio_file_path = os.path.join(subdir_path, "audio.mp3")
        transcript_path = os.path.join(subdir_path, "transcript.json")


        with open(transcript_path, "w") as file:
            file.write(json.dumps({"callid": subdir, "transcript": "in progress..."}))

        audio_file = request.files['audioFile']
        audio_file.save(audio_file_path)
        print(audio_file_path)

        # Invoke Whisper AI
        command = f'whisper audio.mp3 --model medium.en'
        result = subprocess.run(command, shell=True, cwd=subdir_path, capture_output=True, text=True)

        # Assume the transcript is written to 'audio.txt' by the above command
        audio_txt_path = os.path.join(subdir_path, "audio.txt")
        with open(audio_txt_path, "r") as file:
            transcript = file.read()

        transcript = transcript.replace("\n", " ").replace("\r", " ").replace("\t", " ")
        print("Transcript:", transcript)
        info = transcript_parser.gpt_response(transcript)
        print("Info:", info)

        complaints_str = info["complaints"]
        past_medical_history_str = info["past medical history"]
        current_complaints = [complaint.strip().lower() for complaint in complaints_str.split(",")]
        past_medical_history = [history.strip().lower() for history in past_medical_history_str.split(",")]
        
        out = transcript_parser.compute_similarity(current_complaints, past_medical_history)
        print(out)
        triage = transcript_parser.get_triage(out)
        print("triage:", triage)
        # Write the callid and transcript to a json
        with open(transcript_path, "w") as file:
            file.write(json.dumps({"callid": subdir, "transcript": transcript}))

        return jsonify({'callid': subdir}), 200
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
        callids.sort()
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

