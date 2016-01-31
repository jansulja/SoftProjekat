from __future__ import division

class Note:
    def __init__(self, pitch_name, relative_duration=0.25, tempo=180):
        self.pitch_name = pitch_name
        self.duration = (240/tempo) * relative_duration
        self.set_frequency()

    def print_note(self):
        print self.pitch_name
        print self.duration
        #print self.frequency

    def get_frequency(self):
        return self.frequency


    def set_duration(self,relative_duration):
        self.duration = (240/180) * relative_duration

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

