# 선거시스템
#  유권자 들은 기호로 투표를 진행 결과를 리스트에 저장
# ex 1,2,3
# 투표는 순환문은 이용헤서 유권자가 10이라면 10번순환하면서 후보자(1~5)선택
#[1,1,2,3,4,1,5,1]
# 리스트에 있는 각번호의 횟수를 구해서 당선자를 출력
candidate = ['홍길동','이순신','강감찬','율곡','신사임당']
vote = []
counts = 10
# input('투표를하세요(1~5) :')

#투표진행
import random
for i in counts:
    vote.append(int(input('투표를 하세요(1~5) : ')))
print(f'vote = {vote}')
result ={}
#dict 기능을 이용

for i in vote: #1~5
    if i in result:
        result[i] +=1
    else:
        result[i] = 1
print(f'result = {result}')