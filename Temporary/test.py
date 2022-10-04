
def test(a,b,d=1,e=2):
    c=a+b

    def testa(f,d=1,e=2):
        g=f+d+e
        return g
    return testa

h=test(1,2)
print(h(1,d=2,e=3))