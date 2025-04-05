import os
from flask import Flask, render_template, request, jsonify
from music21 import converter, note, chord

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'midi', 'mid'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_notes(midi_path):
    try:
        score = converter.parse(midi_path)

        letter_notes = []

        for part in score.parts:
            for element in part.flat.notes:
                if isinstance(element, note.Note): 
                    letter_notes.append({'note': element.name, 'time': float(element.offset)})
                elif isinstance(element, chord.Chord): 
                    note_names = '.'.join(n.name for n in element.notes)
                    letter_notes.append({'note': note_names, 'time': float(element.offset)})

        letter_notes.sort(key=lambda x: x['time'])
        return letter_notes

    except Exception as e:
        print(f"Error generating notes: {e}")
        return []

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        
        notes_data = generate_notes(filename)
        if notes_data:
            return jsonify(notes_data)
        else:
            return jsonify({'error': 'Error parsing MIDI file'}), 500
    else:
        return jsonify({'error': 'Invalid file type'}), 400

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
