class Scale(object):
   def __init__(self, base, cap, stepper):
      self.base = base
      self.cap = cap
      self.stepper = stepper
      self.current = base

   def __next__(self):
      if self.current < self.cap:
         old = self.current
         self.current = self.stepper(self.current)
         return old
      else:
         raise StopIteration

   def __iter__(self):
      return self

doubler = lambda a, b: Scale(a, b, lambda y: 2*y)
adder = lambda a, b, inc: Scale(a, b, lambda y: y + inc)


