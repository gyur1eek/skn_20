#다양한 매개변수
    #기본매개변수 default parameter

def myAdd(num1, num2):
    return num1 + num2

result = myAdd(10,20)
print(f'result = {result}')

def mon(num1, num2=5):
    return num1 + num2

result =mon(10,39)
print(f'result = {result}')

result =mon(5)
print(f'result = {result}')
