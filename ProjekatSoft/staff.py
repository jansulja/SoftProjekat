import chord as ch
import bar
class Staff:

    def __init__(self,staff_num,regions,groups,bar_lines,accidentals):
        print 'staff num: ' + str(staff_num) + ' lines: ' + str(groups[staff_num])
        self.bar_lines = bar_lines
        self.accidentals = accidentals
        self.groups = groups
        self.staff_num = staff_num
        self.regions = regions
        self.chord_regs = self.create_chords()

        self.bars = []
        self.generate_bars()
        self.fill_bars()
        self.print_bars()

    def print_bars(self):
        for bar in self.bars:
            bar.print_bar()

    def fill_bars(self):

        for acc in self.accidentals:
            for bar in self.bars:
                if acc.x > bar.start and acc.x<bar.end:
                    bar.add_acc(acc)



        for i in range(len(self.chord_regs)):
            for bar in self.bars:
                if self.chord_regs[i][0].x > bar.start and self.chord_regs[i][0].x<bar.end:
                    bar.add_chord(self.chord_regs[i])

        for bar in self.bars:
            bar.generate_accs()

        for bar in self.bars:
            bar.generate_chords()


    def generate_bars(self):
        bars = []
        for i in range(len(self.bar_lines)-1):
            bars.append(bar.Bar(i,self.bar_lines[i],self.bar_lines[i+1],self.groups[self.staff_num]))
        self.bars = bars

    def create_chords(self):

        chord_regs = []


        for reg in self.regions:
            index = self.find_chord(chord_regs,reg)
            if index == -1:
                new_chord = []
                new_chord.append(reg)
                chord_regs.append(new_chord)
            else:
                chord_regs[index].append(reg)

        return chord_regs



    def find_chord(self,regs,reg):

        chord_idx = -1
        for i in range(len(regs)):
            if len(regs[i])>0:
                if abs(regs[i][0].x - reg.x) < 5:
                    chord_idx = i

        return chord_idx


    def get_chords(self):
        chords = []
        for bar in self.bars:
            chords += bar.chords

        return chords


