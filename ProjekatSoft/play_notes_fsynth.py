import time
import fluidsynth

def play_notes(notes,sound_font):


    fs = fluidsynth.Synth()
    fs.start()
    sfid = fs.sfload("sound_fonts/" + sound_font)
    fs.program_select(0, sfid, 0, 0)

    for i in range(len(notes)):
        lenth = notes[i].duration
        frequency = notes[i].frequency
        note_name = str(notes[i].pitch_name)
        midinum = notes[i].midinum
        velocity = 30


        if note_name.startswith('rest'):
            time.sleep(lenth)
        else:
            fs.noteon(0, midinum, velocity)
            time.sleep(lenth)
            fs.noteoff(0,midinum)
            time.sleep(lenth)

    fs.delete()