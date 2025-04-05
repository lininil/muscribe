import time
from music21 import *
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Function to parse the MIDI file and generate notes and their onset times
def generate_notes():
    try:
        # Load the MIDI file
        score = converter.parse("twinkle.mid")

        letter_notes = []

        for part in score.parts:
            for element in part.flat.notes:
                if isinstance(element, note.Note):  # Single note
                    # Convert the onset time from Fraction to float
                    letter_notes.append({'note': element.name, 'time': float(element.offset)})
                elif isinstance(element, chord.Chord):  # Chords
                    note_names = '.'.join(n.name for n in element.notes)
                    # Convert the onset time from Fraction to float
                    letter_notes.append({'note': note_names, 'time': float(element.offset)})

        letter_notes.sort(key=lambda x: x['time'])  # Sort by onset time
        return letter_notes

    except Exception as e:
        print(f"Error generating notes: {e}")
        return []

# Flask route to serve the main page
@app.route('/')
def index():
    return render_template('index.html')

# API route to get notes data as JSON
@app.route('/get_notes')
def get_notes():
    try:
        notes_data = generate_notes()
        if notes_data:
            return jsonify(notes_data)
        else:
            return jsonify({'error': 'No notes found or error parsing MIDI file'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
