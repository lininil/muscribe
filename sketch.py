from music21 import *

score = converter.parse("twinkle.mid") 

letter_notes = []
for part in score.parts:
    for element in part.flat.notes:
        if isinstance(element, note.Note): 
            letter_notes.append(element.name)
        elif isinstance(element, chord.Chord): 
            letter_notes.append('.'.join(n.name for n in element.notes))

print(" ".join(letter_notes))

