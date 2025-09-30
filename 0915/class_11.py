class Student:
    def study(self):
        return "공부중입니다"
class teacher:
    def teach(self):
        return "가르치는 중입니다."
    
#리스트에 어떤 객체가 있는지 모를 때 특정 인스턴스만 기대할 수 없다
peoples =  [Student(), Teacher(), Student()]
peoples[0].teach()