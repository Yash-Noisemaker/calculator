def add(a,b):
    print("Result:",a + b)

def sub(a,b):
    print("Result:",a - b)

def mul(a,b):
    print("Result:",a * b)

def divi(a,b):
    if b != 0:
        print("Result:",a / b)
    else:
        print("Cannot be divided by 0")
    

def calcu():
    print("\n :) Calculate")
    
    num1 = eval(input("Entre value: "))
    op = input("Enter operation: ")
    num2 = eval(input("Entre value: "))


    
    if op == "+":
        add(num1,num2)

    elif op == "-":
        sub(num1,num2)

    elif op == "*":
        mul(num1,num2)

    elif op == "/":
        divi(num1,num2)

    else:
        print("Error")




calcu()