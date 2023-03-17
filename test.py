from datetime import datetime

origin = "Hôm nay trời nắng đẹp"

sub = "Troi"

index = origin.find(sub)

right_border = (len(sub) + index >= len(origin)) or (origin[len(sub) + index] in (" ", "\n"))
left_border = (index-1 < 0) or (origin[index-1] == " ")

if(left_border and right_border):
    print("YES")
    print(origin[index], origin[index+1], origin[index-1])
else:
    print("NO")
    
print(origin.encode("utf-8"))
print(sub.encode("utf-8"))