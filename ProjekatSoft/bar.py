import accidental as acc
import region as reg
import chord as ch
class Bar:
    def __init__(self,id,start,end,lines):
        self.id = id
        self.start = start.x
        self.end = end.x
        self.lines = lines
        self.acc_regs = []
        self.accs = []
        self.chords = []
        self.chord_regs = []
        self.all_symbols = []
        self.acc_state = {
            'A3': 0,
            'H3': 0,
            'C4': 0,
            'D4': 0,
            'E4': 0,
            'F4': 0,
            'G4': 0,
            'A4': 0,
            'H4': 0,
            'C5': 0,
            'D5': 0,
            'E5': 0,
            'F5': 0,
            'G5': 0,
            'A5': 0,
            'H5': 0,
        }

    def generate_accs(self):
        for i in range(0,len(self.acc_regs)-1,2):
            self.accs.append(acc.Accidental(self.acc_regs[i],self.acc_regs[i+1],self.lines))

        self.all_symbols = self.accs + self.chord_regs



        for i in range(len(self.all_symbols)-1):
            for j in range(i+1,len(self.all_symbols)):
                if self.get_x_for_symbol(j)<self.get_x_for_symbol(i):
                    pom = self.all_symbols[i]
                    self.all_symbols[i] = self.all_symbols[j]
                    self.all_symbols[j] = pom




    def get_x_for_symbol(self,i):
            obj = self.all_symbols[i]
            if isinstance(obj,list):
                return obj[0].x
            else:
                return obj.x1


    def add_acc(self,acc):
        self.acc_regs.append(acc)


    def add_chord(self,chord):
        self.chord_regs.append(chord)

    def print_bar(self):
        print '-------------------------'
        print self.id,self.start,self.end
        print 'Chords'
        for chord in self.chords:
            print chord.print_chord()
        print 'Accidentals'
        for ac in self.accs:
            print 'y1= ',ac.y1,'y2= ',ac.y2
            print ac.pitch

    def generate_chords(self):


        chord_regs = []

        for symbol in self.all_symbols:

            if isinstance(symbol,acc.Accidental):
                if(not str(symbol.pitch).startswith('No')):
                    if self.acc_state[symbol.pitch] == 0:
                        self.acc_state[symbol.pitch] = 1
                    else:
                        self.acc_state[symbol.pitch] = 0

            else:
                self.chords.append(ch.Chord(symbol,self.lines,self.acc_state))




