from operations.add import suma
from operations.subtraction import subtraction
from operations.multiplication import multiplication
from operations.division import division

def calculate():
    num1 = float(input("Enter the first number: "))
    num2 = float(input("Enter the second number: "))

    print("Addition: ", suma(num1,num2))
    print("Subtraction: ", subtraction(num1,num2))
    print("Multiplication: ", multiplication(num1,num2))
    print("Division: ", division(num1,num2))

calculate()