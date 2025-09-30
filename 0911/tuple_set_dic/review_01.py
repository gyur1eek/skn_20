# 딕셔너리
    #.items(), .keys(), .values()
# 정렬
    # sorted()
# max
    # max()
# enumerate
    # 순환문에서 리스트를 감싸면 (인덱스, 라스트의 값)
# zip()
    #여러개의 iterable 들을 각 웒소를 쌍으로 하는 집합
    # (1,2), ('사과','배')
    # [ (1,'사과'), (2,'배')]
# map()
    #iterable한 객체의 각 요소에 특정 함수를 적용
    # map(int, ['1','2'])-> 1,2

import collections
datas = [1,1,1,1,2,1,3,4,1,2,4,1]
print(collections.Counter(datas))
