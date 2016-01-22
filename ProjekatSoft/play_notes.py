import math
import pyaudio


def playNotes(notes):

    #sudo apt-get install python-pyaudio
    PyAudio = pyaudio.PyAudio

    #See http://en.wikipedia.org/wiki/Bit_rate#Audio
    BITRATE = 16000 #number of frames per second/frameset.

    #See http://www.phy.mtu.edu/~suits/notefreqs.html
    #FREQUENCY = 261.63 #Hz, waves per second, 261.63=C4-note.
    #LENGTH = 1.2232 #seconds to play sound

    p = PyAudio()
    stream = p.open(format = p.get_format_from_width(1),
                    channels = 1,
                    rate = BITRATE,
                    output = True)
    WAVEDATA = ''
    for i in range(len(notes)):
        lenth = notes[i].duration
        frequency = notes[i].frequency

        NUMBEROFFRAMES = int(BITRATE * lenth)
        RESTFRAMES = NUMBEROFFRAMES % BITRATE


        for x in xrange(NUMBEROFFRAMES):
         WAVEDATA = WAVEDATA+chr(int(math.sin(x/((BITRATE/frequency)/math.pi))*127+128))

        #fill remainder of frameset with silence
        #for x in xrange(RESTFRAMES):
         #WAVEDATA = WAVEDATA+chr(128)


    stream.write(WAVEDATA)

    stream.stop_stream()
    stream.close()
    p.terminate()