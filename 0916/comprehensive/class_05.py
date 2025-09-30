from abc import ABC, abstractmethod
class Parents(ABC):
    def make_money(self):
        raise NotImplementedError

    @abstractmethod
    def save_money(self):
        pass

class Child(Parents):
    def make_money(self): #부모의 make_money 재정의(override)
        print('장사')

    def save_money(self):
        print('투자')
        
        
c = Child()
c.make_money() #다형성
