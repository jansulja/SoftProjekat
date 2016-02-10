class Accidental:
    def __init__(self,reg1,reg2,lines):
        self.x1 = reg1.x
        self.x2 = reg2.x
        self.y1 = reg1.y
        self.y2 = reg2.y
        self.w1 = reg1.w
        self.w2 = reg2.w
        self.h1 = reg1.h
        self.h2 = reg2.h


        self.lines = lines
        self.pitch = 'No pitch'
        self.added_lines = self.add_extra_lines()
        self.set_pitch()


    def add_extra_lines(self):
        extra_lines = []
        for i in range(len(self.lines)-1):
            extra_lines.append(self.lines[i])
            extra_lines.append(self.lines[i] - (self.lines[i]-self.lines[i+1])/2)

        extra_lines.append(self.lines[-1])
        return extra_lines

    def set_pitch(self):
        for i in range(len(self.added_lines)):
            #print 'line:  ' + str(self.added_lines[i]) + ' y1 = ' + str(self.y1) + ' y2 = ' + str(self.y2)
            if self.added_lines[i] > self.y2 and self.added_lines[i]<self.y1:
                #print 'setting pitch for : ' +str(i)
                self.pitch = self.get_pitch_name(i)



    def get_pitch_name(self,i):

        pitch_names =  {
            0: 'A3',
            1: 'H3',
            2: 'C4',
            3: 'D4',
            4: 'E4',
            5: 'F4',
            6: 'G4',
            7: 'A4',
            8: 'H4',
            9: 'C5',
            10: 'D5',
            11: 'E5',
            12: 'F5',
            13: 'G5',
            14: 'A5',
            15: 'H5'
        }
        return pitch_names[i]