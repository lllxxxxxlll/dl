class A:
    def __init__(self):
        print("SA")
        print("OA")
class B(A):
    def __init__(self):
        print("SB")
        A.__init__(self)
        print("OB")
class C(A):
    def __init__(self):
        print("SC")
        A.__init__(self)
        print("OC")
class S(B,C):
    def __init__(self):
        print("SS")
        C.__init__(self)
        B.__init__(self)
        print("OS")
S()