import fluidsynth
import time
class Player:
    def __init__(self,sheet):
        self.sheet = sheet
        self.staffs = sheet.staffs

    # def play_sheet(self):
    #
    #     fs = fluidsynth.Synth()
    #     fs.start()
    #     sfid = fs.sfload("sound_fonts/JR_organ.sf2")
    #     fs.program_select(0, sfid, 0, 0)
    #
    #     for staff in reversed(self.staffs):
    #         chords = staff.get_chords()
    #         print chords
    #         for chord in chords:
    #             print chord
    #             for note in chord.notes:
    #                 lenth = note.duration
    #                 midinum = note.midinum
    #                 velocity = 30
    #                 fs.noteon(0, midinum, velocity)
    #             time.sleep(0.5)
    #             for note in chord.notes:
    #                 lenth = note.duration
    #                 midinum = note.midinum
    #                 velocity = 30
    #                 fs.noteoff(0, midinum)
    #             time.sleep(0.5)

    def play_sheet(self, chords, sound_font):

        fs = fluidsynth.Synth()
        fs.start()
        sfid = fs.sfload("sound_fonts/" + sound_font)
        fs.program_select(0, sfid, 0, 0)

        for chord in chords:

            for note in chord.notes:
                midinum = note.midinum
                velocity = 30
                fs.noteon(0, midinum, velocity)
            time.sleep(chord.duration)
            for note in chord.notes:
                lenth = note.duration
                midinum = note.midinum
                velocity = 30
                fs.noteoff(0, midinum)
            time.sleep(chord.duration)