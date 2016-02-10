class Region:
    def __init__(self,x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def to_string(self):
        return "Region: " + str(self.x,self.y,self.w,self.h)