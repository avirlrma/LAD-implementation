#input is set of +ve patterns, points
#output should be subset of the patterns

from term import *

class Theory:
    def __init__(self, lad):
        self.lad = lad
        self.positive_patterns = lad.generate_patterns(5)
        self.negative_patterns = lad.generate_patterns(5,False)

    def select_patterns(self,positive=True):
        if not positive:
            B_prim = self.lad.B_minus
            pattern = self.negative_patterns
        else:
            B_prim = self.lad.B_plus
            pattern = self.positive_patterns

        ss = {x:x.eval_set(B_prim) for x in pattern}
        temp =  set()
        sel_patterns = []
        ss = sorted(ss.items(),key=lambda x: -len(x[1]))

        i=0
        while len(temp)!=len(B_prim):
            temp.update(ss[i][1])
            sel_patterns.append(ss[i][0])
            i+=1
        return sel_patterns
    
    def calculate_weights(self,pattern,positive=True):
        mul=1
        if not positive:
            B_prim = self.lad.B_minus
            mul = -1
        else:
            B_prim = self.lad.B_plus

        ss = {x:len(x.eval_set(B_prim)) for x in pattern}
        normalizing_val = sum(ss.values())
        ss = {x:mul*y/normalizing_val for x,y in ss.items()}
        return ss
        

