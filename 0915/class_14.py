#클래스
#클래스 변수, 인스턴스 변수
# 생성자 __init__
# 메소드 __str__, __eq__, , __ne__, __lt__, __le__, __gt__, __ge__
# property
# 객체생성

# 상품관리
#  상품명 product_name, 가격 product_price, 재고 product_stock

import random
class Product:
    def __init__ (self, name, price, stock):
        self.product_name = name
        self.product_price = price
        self.product_stock = stock  
    def __str__(self, stock):
        if stock > 0:
            print("재고는 음수가 될 수 없습니다.")
        else:
            self.product_stock = stock

p = Product("아이폰", 1000000, 5)