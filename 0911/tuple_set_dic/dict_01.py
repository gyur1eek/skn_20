# dict
# 키와 값의 쌍으로 구성
# 순서가 없다
# 키는 중복 안됨
# 키는 변하지 않는 자료형만 가능(문자열, 숫자, 튜플)
# CRUD 가능 *CRUD(데이터생성, 데이터읽기, 데이터수정, 데이터삭제)
# 각 요소에 접근할 때는 키값을 접근(인덱스가 아님)
student = {
    "name" : "홍길동",
    "age" : 20,
    "major" : "컴퓨터"
}
#읽기
print(f"student['name'] = {student['name']}")
#업데이트
student['name'] = '이순신'
print(f'student = {student}')
#삭제
del student['name']
print(f'student = {student}')
#추가
student['addr'] = '서울시 강남구'
print(f'student = {student}')