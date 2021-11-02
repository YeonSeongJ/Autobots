"""

print("도전문제 2.6")
print("\n(1) 사용자로부터 체중과 신장을 입력하도록 하여, 입력된 값에 따라 BMI를 계산하는 스크립트를 작성하라.")

weight = input("\n체중을 입력하시오(kg): ")
height = input("신장을 입력하시오(m): ")
print("당신의 BMI는 ", float(weight) / (float(height)**2), "입니다.")



print("\n\n\n(2) 사용자로부터 두 수를 입력받아 두 수의 합과 평균을 출력하는 프로그램을 작성하여라.")

a1 = float(input("\n첫 번째 숫자를 입력하시오: "))
a2 = float(input("두 번째 숫자를 입력하시오: "))
print("두 수의 합은", a1 + a2, "이고", "두 수의 평균은", (a1 + a2) / 2, "입니다.")



print("\n\n\n(3) 사용자로부터 세 수를 입력받아 세 수의 합과 평균을 출력하는 프로그램을 작성하여라.")

b1, b2, b3= map(float, input("\n세 수를 입력하시오: ").split())
c1 = b1 + b2 + b3
c2 = (b1 + b2 + b3) / 3
print("두 수의 합은", c1, "이고", "두 수의 평균은", c2, "입니다.")



print("\n\n\n도전문제 2.9")
print("\n섭씨 온도를 화씨온도로 바꾸시오")

cel = int(input("\n섭씨온도를 입력하세요 : "))
fah = (9/5) * cel +32
print("섭씨", cel, "도는 화씨로", fah, "도 입니다.")



print("\n\n\n도전문제 3.1")
print("\n사용자가 초를 입력하면 입력된 초가 몇 시간 몇 분 몇 초에 해당하는지 프로그램을 작성하여라")

time = int(input("\n초를 입력해주세요: "))
hour = time / 3600
minute = time % 3600 / 60
second = time % 3600 % 60 
print("입력한 시간은", int(hour), "시간", int(minute), "분", int(second), "초 입니다")



print("\n\n\n도전문제 3.2")

s = int(input("\n여성이면 1, 남성이면 0을 입력하세요: "))
h = int(input("당신의 키는 얼마입니까?(cm) "))
w = float(input("당신의 허리둘레는 얼마입니까?(cm) "))
print("당신의 RFM은", 64 - (20 * (h / w)) + 12 * s, "입니다")



print("도전문제 4.6\n")
age = int(input("나이를 입력해주세요\n"))
if age>= 15 :
    print("본 영화를 보실 수 있습니다")
    print("영화의 가격은 10000원 입니다")
else :
    print("영화를 보실 수 없습니다")
    print("다른 영화를 보시겠어요?")
          

age2 = input("\n교통카드의 유형를 선택하세요(청소년, 성인)\n")
if age2 == "청소년" :
    print("청소년입니다")
else :
    if age2 == "성인" :
        print("승인되었습니다")
    else :
        print("잘못된 유형입니다")



import turtle as t


for i in range(6) :
    t.forward(100)
    t.left(60)
t.penup()
t.forward(222)
t.pendown()
for i in range(8) :
    t.forward(100)
    t.left(45)




print("\n\n구구단 만들기\n")
num = 1
re = 0
while num < 9 :
    num += 1
    count = 1
    while count <= 9 :
        re = num * count
        print('{} * {} = {}'.format(num, count, re)) # 형식을 다르게 3줄작성
#        print("%d * %d = %d" % (num, count, re))
#        print(f'{num} * {count} = {re}')
        count += 1
        if count > 9 : 
            print("\n")

num2 = 1
re2 = 0
for _ in range(8) :
    num2 += 1
    count2 = 1
    for _ in range(9) :
        re2 = num2 * count2
        print('{} * {} = {}'.format(num2, count2, re2))
#        print("%d * %d = %d" % (num2, count2, re2))
#        print(f'{num2} * {count2} = {re2}')
        count2 += 1
        if count2 > 9 : 
            print("\n")

"""

# for i in range(1, 10, 2):
#     for k in range(1, 10):
#         print('%d * %d = %d' % (i, k, i * k))
#     print()

"""
print("\n\n도전과제 5.12\n")
word = input("단어를 입력하세요\n")
for w in word :
    if w in ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U'] :
        break
    else :
        print(w, end='')
        continue
"""

"""
python 

주석
#

변수
get set

연산자
단항    /, //, %
이항

흐름제어문
if for while

break
continue

method - 클래스의 멤버 메서드

function - 프로그램의 유지 보수를 돕고 효율성을 높이기 위한 코드의 집합 

def name(param):
    
    return 
"""

for i in range(1,3,10):
    print(i)


lists = [1] * 5

a = 2

a += 1 if a == 1 else 3

print(a)