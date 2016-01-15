from __future__ import division
import numpy as np
import ann_functions as ann_fun
import soundGenerator as sgen
import play_notes

def play(ann,notes,inputs,outputs,alphabet):

    results = ann.predict(np.array(inputs, np.float32))
    res = ann_fun.display_result(results,alphabet)

    print "asdas"
    print len(res)
    print len(notes)

    for i in range(0, len(res)-2):
        notes[i].print_note()
        print res[i+2]
        notes[i].set_duration(1/int(res[i+2]))
    '''
    for i in range(len(notes)):
        notes[i].print_note()
        sgen.playNote(notes[i].frequency, notes[i].duration)
    '''

    play_notes.playNotes(notes)

