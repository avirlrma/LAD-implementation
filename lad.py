from term import *

#todo: add hamming distance & monotone??

class LAD:
  def __init__(self, n, B_plus, B_minus):
    self.n = n
    self.B_plus = B_plus
    self.B_minus = B_minus

  def generate_patterns(self, D, postive_patterns=True):
    #init
    P = set()
    C = [[empty_term()] for i in range(D+1)]
    B_primary,B_secondary = ((self.B_minus,self.B_plus),(self.B_plus,self.B_minus))\
      [postive_patterns]
    
    for d in range(1, D+1):
      for T in C[d-1]:
        p = T.max_index
        for s in range(p+1, self.n+1):
          for l_new in (s, -s):
            T_ = T.clone()
            T_.add_literal(l_new)
            for T__ in T_.get_literals_with_one_term_dropped():
              if T__ not in C[d-1]:
                # goto <>
                break
            else:
              if any(T_.eval_at_point(q) for q in B_primary):
                if not any(T_.eval_at_point(q) for q in B_secondary):
                  P.add(T_)
                elif d < D:
                  C[d].append(T_)
            # <>
    return P


if __name__ == "__main__":
  B_pls = list(map(make_point, [(1,1,0),(0,1,0),(1,0,1)]))
  B_mns = list(map(make_point, [(1,0,0),(0,0,1),(0,0,0)]))
  n = 3

  lad = LAD(n, B_pls, B_mns)
  print(lad.generate_patterns(5,False))
