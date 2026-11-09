a=0
for i in range(2000,2501):
    if i%4==0 and i%100!=0 or i%400==0:
        a=i
        print(a)

