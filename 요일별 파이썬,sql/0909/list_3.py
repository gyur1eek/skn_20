list_a = [1,2,3]
list_b = [4,5,6]
last_name = '홍'
first_name = '길동'
# 리스트 연산
print(f'list_a + list_b = {list_a + list_b}')
print(f'list_a*2= {last_name*2}')

print(f'last_name + first_name = {last_name + first_name}')
print(f'lst_name*2 = {last_name*2}')

list_c= [
    list_a[0] + list_b[0], 
    list_a[1] + list_b[1], 
    list_a[2] + list_b[2]
]
print(list_c)

#리스트를 선언합니다.
list_a = [1,2,3]

#리스트 뒤에 요소 추가하기
print("#리스트 뒤에 요소 추가하기")
list_a.append(4)
list_a.append(5)
print(list_a)
print()

list_a = [1,2,3]
list_a.extend([4,5,6])
print(list_a)

list_a += [4,5,6]