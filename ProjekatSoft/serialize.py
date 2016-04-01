import pickle

class Serialize:

    def __init__(self,filename,object):
        self.filename = filename
        self.object = object

    def save(self):
        with open('saved_ann/'+self.filename, 'wb') as output:
            pickle.dump(self.object, output, pickle.HIGHEST_PROTOCOL)


