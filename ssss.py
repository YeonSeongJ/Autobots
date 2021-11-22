#직선의 방정식 활용
A = leftIMG[0][:2]
B = leftIMG[0][2:4]

# 기울기
angle = (A[0] - B[0]) / (A[1] - B[1])
BBB = A[0] - angle * A[1]

print('A :', A, 'B :', B)
print(BBB)