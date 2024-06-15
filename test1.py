# basic tests
from me_1 import order, MatchingEngine

# place buy order
o1 = order("John", 1, "buy", 100, 10)
me = MatchingEngine()
me.placeOrder(o1)
assert me.returnState == [o1,None], me.returnState