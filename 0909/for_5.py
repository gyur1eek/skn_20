#중첩for2

list_1 = [10,20,30]
list_2 = [11,22,33]

list_2th = [list_1, list_2]
print(list_2th)
for row in list_2th:
    print(row)

for i in range(len(list_2th)):
    for j in range(len(list_1)):
        print(f'list_2th[{i}][{j}]) {list_2th[i][j]}')


list_of_list = [
    [1,2,3],
    [4,5,6,7],
    [8,9]
]

