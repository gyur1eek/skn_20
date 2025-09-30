#파이썬 클래스에서 getter setter 사용법
import random
class Person:
    def __init__(self, name, age):
        self.__name = name  # private 변수
        self.__age = age    # private 변수

def name(self):
    return self.__name
@name.setter
def name(self, name):
    self.__name = name

p = Person('홍길동', 30)
print(p.name)  
print(p.age)
p.name = "김철수"
p.age = 35