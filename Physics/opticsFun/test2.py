class O1:
    def __init__(self, a="a", b="b", c="c"):
        self.a = a
        self.b = b
        self.c = c

class O2(O1):
    def __init__(self, a="1", b="2", c="3"):
        super().__init__(a, b, c)


o1 = O1()
o2 = O2()
print(o1.a, o2.a)