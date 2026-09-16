def divide(a,b):
    if b==0:
        raise ValueError("b cannot be zero")
    return a / b

def classify_number(x):
    if x>0:
        return "positive"
    if x<0:
        return "negative"
    return "zero"
