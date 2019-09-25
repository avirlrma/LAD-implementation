import copy

__all__ = ['Term', 'empty_term', 'make_point']

class Term:
  def __init__(self):
    self._pos_lits = 0
    self._neg_lits = 0

    self.max_index = 0
    self.last_index = 0

  def add_literal(self, lit):
    if lit > 0:
      self._pos_lits |= 1 << (+lit)
    else:
      self._neg_lits |= 1 << (-lit)
    self.max_index = max(self.max_index, abs(lit))
    self.last_index = lit

  def add_literals(self, lits):
    for lit in lits:
      self.add_literal(lit)

  def eval_at_point(self, p):
    return (p & self._pos_lits) == self._pos_lits and (p & self._neg_lits) == 0

  def clone(self):
    return copy.deepcopy(self)

  def get_literals_with_one_term_dropped(self):
    tmp = 2
    for i in range(1, self.max_index):
      if self._pos_lits & tmp:
        term = self.clone()
        term._pos_lits ^= tmp
        yield term

      if self._neg_lits & tmp:
        term = self.clone()
        term._neg_lits ^= tmp
        yield term
      tmp <<= 1

    if self.last_index < 0 and self._pos_lits & tmp:
      term = self.clone()
      term._pos_lits ^= tmp
      yield term

  def __eq__(self, other):
    return  self._pos_lits  == other._pos_lits  and \
            self._neg_lits  == other._neg_lits

  def __hash__(self):
    return hash((self._pos_lits, self._neg_lits))

  def __repr__(self):
    x = 1
    rep = ""
    for i in range(32):
        a = (x & self._pos_lits)>0
        b = (x & self._neg_lits)>0
        rep += ("x" +str(i) + ", ")*int(a) +\
         ("~" + "x" +str(i) + ", ")*int(b)
        x*=2
    rep = rep[:-2]

    return 'Term<{}>'.format(rep)


def empty_term():
  return Term()

def make_point(xs):
  p = 0
  for i, x in enumerate(xs, 1):
    p |= x << i
  return p

if __name__ == "__main__":

  term = Term()

  term.add_literals([1,-2,3,4])

  p = make_point((1, 0, 1, 1))

  print(term.eval_at_point(p))
