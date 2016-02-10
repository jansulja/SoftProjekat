from __future__ import division

class Note:
    def __init__(self, pitch_name, relative_duration=0.25, tempo=360):
        self.pitch_name = pitch_name
        self.duration = (240/tempo) * relative_duration
        self.set_frequency()
        self.set_midinum()

    def print_note(self):
        print self.pitch_name
        print self.duration
        #print self.frequency

    def get_frequency(self):
        return self.frequency


    def set_duration(self,relative_duration):
        self.duration = (240/300) * relative_duration

    def set_frequency(self):

        tone_frequency =  {

            'G3': 196.00,
            'A3': 220.00,
            'H3': 246.94,

            'C4': 261.63,
            'D4': 293.66,
            'E4': 329.63,
            'F4': 349.23,
            'G4': 392.00,
            'A4': 440.00,
            'H4': 493.88,

            'C5': 523.25,
            'D5': 587.33,
            'E5': 659.25,
            'F5': 698.46,
            'G5': 783.99,
            'A5': 880.00,
            'H5': 987.77,
            'C6': 1046.50
        }

        if tone_frequency.__contains__(self.pitch_name):
            self.frequency = tone_frequency[self.pitch_name]
        else:
            self.frequency = tone_frequency['C4']

    def set_midinum(self):

        midinums =  {


            'A3': 57,

            'A#3': 58,
            'H3': 59,

            'C4': 60,
            'C#4': 61,
            'D4': 62,
            'D#4': 63,
            'E4': 64,
            'F4': 65,
            'F#4': 66,
            'G4': 67,
            'G#4': 68,
            'A4': 69,
            'A#4': 70,
            'H4': 71,

            'C5': 72,
            'C#5': 73,
            'D5': 74,
            'D#5': 75,
            'E5': 76,
            'F5': 77,
            'F#5': 78,
            'G5': 79,
            'G#5': 80,
            'A5': 81,
            'A#5': 82,
            'H5': 83,
            'C6': 84

        }

        if midinums.__contains__(self.pitch_name):
            self.midinum = midinums[self.pitch_name]
        else:
            self.midinum = midinums['C4']