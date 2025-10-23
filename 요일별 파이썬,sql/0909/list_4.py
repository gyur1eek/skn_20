#랜덤 라이브러리 가져오기
import random

#랜덤 라이브러리중에서 sample
random_numbers = random.sample(range(100),5)
print(random_numbers)

#0~10사이 중에서 랜덤하게 한개 생성
random_int = random.randint(0,10)

random_numbers.append(random_int)

#50이 있는지
print( 50 in random_numbers)
print(random_numbers)

print('-'*50)

# 삭제
del random_numbers[0]
print(random_numbers)

random_numbers.pop(0)
print(random_numbers)

