from typing import List
import enum
import itertools

from lad import LAD, make_point

__all__ = ['Field', 'Binarize']

class Field(enum.Enum):
  Nominal = enum.auto()
  Numerical = enum.auto()


class Binarize(LAD):
  def __init__(self, schema: List[Field], B_plus, B_minus):
    super().__init__(len(schema), B_plus, B_minus)
    self.schema = schema

    self.bvars = []   # binary vars introduced by binarization
    self.preprocess()

    self.binarize()
    self.n = sum(map(len, self.bvars))

  def preprocess(self):
    for idx, field_type in enumerate(self.schema):
      if field_type == Field.Nominal:
        self.preprocess_nominal(idx)
      elif field_type == Field.Numerical:
        self.preprocess_numerical(idx)

  def preprocess_nominal(self, idx):
    vals = {row[idx] for row in itertools.chain(self.B_plus, self.B_minus)}   # can optimise using numpy transpose
    if len(vals) == 2:
      yes = vals.pop()
      self.bvars.append([(lambda yes: lambda x: x == yes)(yes)])
    else:
      self.bvars.append([(lambda val: lambda x: x == val)(val) for val in vals])

  def preprocess_numerical(self, idx):
    vals_plus = {row[idx] for row in self.B_plus}
    vals_minus = {row[idx] for row in self.B_minus}

    vals = sorted(vals_plus | vals_minus)
    cuts = [0.5*(vals[i]+vals[i+1]) for i in range(len(vals)-1)]

    def is_essential(cut):
      return True
    cuts = list(filter(is_essential, cuts))

    bvars = []
    bvars.extend([(lambda cut: lambda x: x >= cut)(cut) for cut in cuts])   # level variables
    bvars.extend([(lambda l, r: lambda x: l <= x < r)(l, r) for l, r in zip(cuts[:-1], cuts[1:])])  # interval variables
    self.bvars.append(bvars)

  def binarize(self):
    def binarize_row(row):
      return tuple(itertools.chain( *(tuple(var(val) for var in bvars) for bvars,val in zip(self.bvars, row)) ))

    self.B_plus = [make_point(binarize_row(row)) for row in self.B_plus]
    self.B_minus = [make_point(binarize_row(row)) for row in self.B_minus]


if __name__ == "__main__":
  S_pls = [
    (1, 'green', 'yes', 31),
    (4, 'blue',  'no',  29),
    (2, 'blue',  'yes', 20),
    (4, 'red',   'no',  22)]
  S_mns = [
    (3, 'red',   'yes', 20),
    (2, 'green', 'no',  14),
    (4, 'green', 'no',   7)]

  schema = [
    Field.Numerical,
    Field.Nominal,
    Field.Nominal,
    Field.Numerical]

  lad = Binarize(schema, S_pls, S_mns)
  print(lad.generate_patterns(2))
