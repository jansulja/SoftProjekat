class Regions:

    def __init__(self,groups):
        self.groups = groups
        self.regions = []


    def add_region(self,region):
        self.regions.append(region)

    def print_regions(self):
        for reg in self.regions:
            print reg.x,reg.y,reg.w,reg.h


    def get_sorted_regions(self):

        sorted_regions = [[] for i in range(len(self.groups))]
        s = []
        for reg in self.regions:
            row = self.find_row(reg)
            sorted_regions[row].append(reg)

        for row in sorted_regions:

            for i in range(len(row)-1):
                for j in range(i+1,len(row)):

                    if row[j].x<row[i].x:
                        pom = row[i]
                        row[i] = row[j]
                        row[j] = pom


        for row in sorted_regions:
            for i in range(len(row)):
                s.append(row[i])

        print 'sorted'
        for reg in s:
            print reg.x,reg.y

        return sorted_regions

    def find_row(self,reg):
        row =0
        for i in range(len(self.groups)):
            if reg.y<self.groups[i][0] and reg.y>self.groups[i][len(self.groups[i])-1]:
                row = i

        return row