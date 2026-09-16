def add(a,b):
    return a+b

def sub(a,b):
    if a>b:
        return a-b
    else:
        return b-a

def Sanjiao_S(a,b,c):
    if a+b>c:
        s=(a+b+c)/2
    if a+c>b:
        s=(a+b+c)/2
    if b+c>a:
        s=(a+b+c)/2
    else:
        return ValueError("a,b,c can not be a sanjiao")