# 가위 바위 보 게임 (컴퓨터vs휴먼)
# 가위 :1 바위 :2 , 보: 3
# 규칙: 컴퓨터가 임의로 숫자를 선택: random
# 인간이 숫자를 입력 : input
# 승패를 기록 
# 3번마다 계속할 지 물어본다    : while

import random
# 1: 가위
# 2: 바위
# 3: 보
# 랜덤하게 선택한 컴퓨터의 값
com_choice = random.randint(1,3)
user_choice = random.randint(1,3)
# 사용자의 값
input("입력(1:가위 2:바위 3: 보) :")
#승패 확인[]
if com_choice == user_choice:
    print('비겼습니다')
else:
   if(com_choice == 1 and user_choice == 2) or \
    (com_choice == 2 and user_choice == 3) or \
    (com_choice == 3 and user_choice == 1) :
    print("당신이 이겼습니다.")
   else:
      print("당신이 졌습니다.")
