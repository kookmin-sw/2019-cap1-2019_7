
f = open("test1.srt", 'w')
num=0
start_time = ["00:00:00,000","00:00:06,400","00:00:12,400","00:00:18,400"]
end_time = ["00:00:05,320","00:00:10,230","00:00:17,230","00:00:22,800"]
str_arrow = " --> "
str_sub = ["ㅎㅇㅎㅇㅎㅇ", "ㅎㅎㅎㅎ", "지금은 자막파일 제작 테스트 중 입니다.", "빠이빠이"]

for x in range(0,4,1):
    num+=1
    f.write(str(num))
    f.write("\n")
    f.write(start_time[x])
    f.write(str_arrow)
    f.write(end_time[x])
    f.write("\n")
    f.write(str_sub[x])
    f.write("\n\n")

f.close()