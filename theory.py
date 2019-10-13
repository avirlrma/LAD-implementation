#input is set of +ve patterns, points
#output should be subset of the patterns

from term import *

class Theory:
    def __init__(self, lad):
        self.lad = lad
        self.positive_patterns = lad.generate_patterns(5)

    def select_patterns(self):
        ss = [x.eval_set(self.lad.B_plus) for x in self.positive_patterns]
        temp =  set()
        ss = sorted(ss,key=lambda x: len(x))
        i=0
        while len(temp)!=len(self.lad.B_plus):
            temp.update(ss[i])
            i+=1
        return temp
    
    def calculate_weights(self):
        

