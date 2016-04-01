from __future__ import division
import staff as st
import chord as ch
class Sheet:

    def __init__(self,sorted_regions,groups,bar_lines,accidentals):
        self.accidentals = accidentals
        self.bar_lines = bar_lines
        self.staffs = []
        self.groups = groups
        for i in range(len(sorted_regions)):
            self.staffs.append(st.Staff(i,sorted_regions[i],groups,bar_lines[i],accidentals[i]))


    def set_chords_duration(self,durations):
        all_chords = []
        for staff in reversed(self.staffs):
            chords = staff.get_chords()
            for chord in chords:
                all_chords.append(chord)


        new_chords = []
        i = 0
        for dur in durations:

            print dur

            if(str(dur).startswith('rest')):
                rest_dur = int(str(dur).split('-')[1])
                rest_chord  = ch.Chord([],[],{})
                rest_chord.set_duration(1/rest_dur)
                new_chords.append(rest_chord)
            elif(str(dur).startswith('acc')):
                continue
            elif(str(dur) == '1' or str(dur) == '2' or str(dur) == '4' or str(dur) == '8'):
                #if i < len(all_chords):
                new_chord = all_chords[i]
                new_chord.set_duration(1/int(dur))
                new_chords.append(new_chord)
                i += 1
            else:
                continue


        return new_chords

    def get_all_chords(self):
        all_chords = []
        for staff in reversed(self.staffs):
            chords = staff.get_chords()
            for chord in chords:
                all_chords.append(chord)

        return all_chords
