# 함수
# 함수명 add
# 파라메터는 2개 op1, op2
# 결과를 반환한다

def add(op1,op2):
    return op1 + op2

def add(op1,op2):
    result = op1 + op2
    return result

# 사용
print( add( 10,30 ))
two_number_hab = add(10,30)
numbers = [add(10,2),add(100,20)]

# 매개변수 받아서 출력하는 함수
# 함수명 : show_number
# 매개변후명 : data
def show_number( data) :
    print(f'numbers = {data}')

show_number(add(10,2))

def hello(hello):
    return(len(hello))

hello = '안녕하세요'
print(len(hello))