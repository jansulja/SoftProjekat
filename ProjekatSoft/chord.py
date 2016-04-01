from __future__ import division
import note as nt
import main_frame as mf

class Chord:

    def __init__(self,regions,lines,acc_state):
        self.tempo = 240
        self.acc_state = acc_state
        self.regions = regions
        self.lines = lines
        self.notes = []
        self.duration = (240/self.tempo) * (1/4)

        self.generate_notes()
        self.print_chord()

    def set_duration(self,relative_duration):
        print 'chord dur ', relative_duration
        self.duration = (240/self.tempo) * relative_duration

    def print_chord(self):
        print 'chord  <--> ' + str(self.duration)
        for note in self.notes:
            print note.pitch_name


    def get_y_positions(self):
        y_pos = []
        for reg in self.regions:
            y_pos.append(reg.y)
        return y_pos



    def generate_notes(self):
        note_positions = self.get_y_positions()
        notes = []

        for note_y in note_positions:
            for i in range(0, len(self.lines)-1):
                if note_y < self.lines[i] and note_y >= self.lines[i+1]:
                    notes.append(self.get_note(i,note_y,self.lines[i]))

        self.notes = notes


    def get_note(self,i,note_y,line_y):

        #print 'i: ' , i ,' note y: ',note_y, 'line_y : ' ,line_y

        if mf.Application.from_notebook == 0:
            #print '@@@'
            constant = 8
        else:
            constant = 8

        if i==0:
            if line_y-note_y < constant:
                if self.acc_state['A3'] == 1:
                    return nt.Note('A#3')
                else:
                    return nt.Note('A3')
            else:
                if self.acc_state['H3'] == 1:
                    return nt.Note('C4')
                else:
                    return nt.Note('H3')
        elif i==1:

            if line_y-note_y < constant:
                if self.acc_state['C4'] == 1:
                    return nt.Note('C#4')
                else:
                    return nt.Note('C4')
            else:
                if self.acc_state['D4'] == 1:
                    return nt.Note('D#4')
                else:
                    return nt.Note('D4')
        elif i==2:
            if line_y-note_y < constant:
                if self.acc_state['E4'] == 1:
                    return nt.Note('F4')
                else:
                    return nt.Note('E4')
            else:
                if self.acc_state['F4'] == 1:
                    return nt.Note('F#4')
                else:
                    return nt.Note('F4')
        elif i==3:
            if line_y-note_y < constant:
                if self.acc_state['G4'] == 1:
                    return nt.Note('G#4')
                else:
                    return nt.Note('G4')
            else:
                if self.acc_state['A4'] == 1:
                    return nt.Note('A#4')
                else:
                    return nt.Note('A4')
        elif i==4:
            if line_y-note_y < constant:
                if self.acc_state['H4'] == 1:
                    return nt.Note('C5')
                else:
                    return nt.Note('H4')
            else:
                if self.acc_state['C5'] == 1:
                    return nt.Note('C#5')
                else:
                    return nt.Note('C5')
        elif i==5:
            if line_y-note_y < constant:
                if self.acc_state['D5'] == 1:
                    return nt.Note('D#5')
                else:
                    return nt.Note('D5')
            else:
                if self.acc_state['E5'] == 1:
                    return nt.Note('F5')
                else:
                    return nt.Note('E5')
        elif i==6:
            if line_y-note_y < constant:
                if self.acc_state['F5'] == 1:
                    return nt.Note('F#5')
                else:
                    return nt.Note('F5')
            else:
                if self.acc_state['G5'] == 1:
                    return nt.Note('G#5')
                else:
                    return nt.Note('G5')
        elif i==7:
            if line_y-note_y < constant:
                if self.acc_state['A5'] == 1:
                    return nt.Note('A#5')
                else:
                    return nt.Note('A5')
            else:
                if self.acc_state['H5'] == 1:
                    return nt.Note('C6')
                else:
                    return nt.Note('H5')
        else:
            print 'note does not match'
        # elif i==8:
        #     if line_y-note_y < 5:
        #         return nt.Note('C6')
        #     else:
        #         return nt.Note('D6')