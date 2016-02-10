from __future__ import division
import numpy as np
import ann_functions as ann_fun
import soundGenerator as sgen
import play_notes
import play_notes_fsynth
import note as nt

def play(ann,notes,inputs,outputs,alphabet,sound_font):

    results = ann.predict(np.array(inputs, np.float32))
    res = ann_fun.display_result(results,alphabet)
    res = replace_beams(res)

    print len(res)
    print len(notes)

    notes_with_rests = []

    note_cnt = 0
    for i in range(2, len(res)):
        symbol = str(res[i])

        if(symbol.startswith('rest')):
            rest = nt.Note(symbol)
            dur = symbol.split('-')[1]
            rest.set_duration(1/int(dur))
            notes_with_rests.append(rest)
        else:
            note = notes[note_cnt]
            note.set_duration(1/int(res[i]))
            notes_with_rests.append(note)
            note_cnt+=1

    for i in range(len(notes_with_rests)):
        notes_with_rests[i].print_note()

    '''
    for i in range(len(notes)):
        notes[i].print_note()
        sgen.playNote(notes[i].frequency, notes[i].duration)
    '''

    #play_notes.playNotes(notes_with_rests)
    play_notes_fsynth.play_notes(notes_with_rests,sound_font)

def replace_beams(results):
        new_res = []
        for i in range(len(results)):
            if results[i] == 'beam-8':
                new_res.append('8')
                new_res.append('8')
            else:
                new_res.append(results[i])

        return new_res