print("------------Task 1------------")

green_line=[ 
"Songshan","Nanjing Sanmin","Taipei Arena","Nanjing Fuxing","Songjiang Nanjing","Zhongshan", 
"Beimen","Ximen","Xiaonanmen","Chiang Kai-shek Memorial Hall","Guting","Taipower Building",
"Gongguan","Wanlong","Jingmei","Dapinglin","Qizhang","Xindian City Hall","Xindian","Xiaobitan"
]

green_line_dict={station: index for index, station in enumerate(green_line)}


messages={
    "Leslie":"I'm at home near Xiaobitan station.", 
    "Bob":"I'm at Ximen MRT station.",
    "Mary":"I have a drink near Jingmei MRT station.", 
    "Copper":"I just saw a concert at Taipei Arena.", 
    "Vivian":"I'm at Xindian station waiting for you."
}

friends_name=list(messages.keys())
friends_place=list(messages.values())

for i in range(len(friends_place)):
    string=friends_place[i]
    for station in green_line:
        if station in string:
            friends_place[i]=station
            break

find_friends_dict=dict(zip(friends_name,friends_place))


def find_and_print(messages, current_station):
    
    if green_line_dict[current_station]<=green_line_dict["Qizhang"]:
        green_line_dict["Xiaobitan"]=green_line_dict["Xindian City Hall"]
        distance=find_friends_dict.copy()
        for name in friends_name:
            distance[name]=abs(green_line_dict[find_friends_dict[name]]-green_line_dict[current_station])
        print(min(distance, key=distance.get))
    

    elif green_line_dict[current_station]>=green_line_dict["Xindian City Hall"]:
        green_line_dict["Xiaobitan"]=green_line_dict["Dapinglin"]
        distance=find_friends_dict.copy()
        for name in friends_name:
            distance[name]=abs(green_line_dict[find_friends_dict[name]]-green_line_dict[current_station])
        print(min(distance, key=distance.get))


    elif current_station=="Xiaobitan":
        green_line_dict["Xiaobitan"]=green_line_dict["Qizhang"]
        distance=find_friends_dict.copy()
        for name in friends_name:
            distance[name]=abs(green_line_dict[find_friends_dict[name]]-green_line_dict[current_station])
        print(min(distance, key=distance.get))


find_and_print(messages, "Wanlong") # print Mary 
find_and_print(messages, "Songshan") # print Copper 
find_and_print(messages, "Qizhang") # print Leslie 
find_and_print(messages, "Ximen") # print Bob 
find_and_print(messages, "Xindian City Hall") # print Vivian


print("------------Task 2------------")

consultants=[
    {"name":"John", "rate":4.5, "price":1000}, 
    {"name":"Bob", "rate":3, "price":1200}, 
    {"name":"Jenny", "rate":3.8, "price":800}
]

consult_member=len(consultants) 
price_sort=sorted(consultants,key=lambda x:x["price"])
rate_sort=sorted(consultants,reverse=True,key=lambda x:x["rate"])
consult_schedule={}
for i in consultants:
    consult_schedule[i["name"]]=[]


def book(consultants, hour, duration, criteria):
    book_hours=[]  

    for i in range(hour,hour+duration):
        book_hours.append(i)

    if criteria=="price": 
        for i in range(consult_member): 
            all_not_in_schedule=True 
            for item in book_hours:
                if item in consult_schedule[price_sort[i]["name"]]:
                    all_not_in_schedule=False
                    break 
            if all_not_in_schedule:
                consult_schedule[price_sort[i]["name"]].extend(book_hours)
                print(price_sort[i]["name"])
                break
        else:
            print("No Service")

    elif criteria=="rate": 
        for i in range(consult_member): 
            all_not_in_schedule=True 
            for item in book_hours:
                if item in consult_schedule[rate_sort[i]["name"]]:
                    all_not_in_schedule=False
                    break 
            if all_not_in_schedule:
                consult_schedule[rate_sort[i]["name"]].extend(book_hours)
                print(rate_sort[i]["name"])
                break
        else:
            print("No Service")
    else:
        print("No Service")


book(consultants, 15, 1, "price") # Jenny 
book(consultants, 11, 2, "price") # Jenny 
book(consultants, 10, 2, "price") # John 
book(consultants, 20, 2, "rate") # John 
book(consultants, 11, 1, "rate")# Bob 
book(consultants, 11, 2, "rate") # No Service 
book(consultants, 14, 3, "price") # John


print("------------Task 3------------")

import collections

def func(*data):

    if not data: 
        print("沒有")
        return  

    uniq_word=[]
    for i in range(len(data)):
        if len(data[i])==2 or len(data[i])==3:
            uniq_word.append(data[i][1])
        elif len(data[i])==4 or len(data[i])==5:
            uniq_word.append(data[i][2])


    my_dict=dict(zip(uniq_word,data))
    count=collections.Counter(uniq_word) 
    rank=count.most_common() 


    if len(rank)==1:
        print(my_dict[rank[0][0]])
    elif rank[-1][1]<rank[-2][1]:
        print(my_dict[rank[-1][0]])
    else:
        print("沒有")

func("彭大牆", "陳王明雅", "吳明") # print 彭大牆
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花") # print 林花花 
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花") # print 沒有 
func("郭宣雅", "夏曼藍波安", "郭宣恆") # print 夏曼藍波安


print("------------Task 4------------")

def get_number(index):
    sequence=[0]
    number=0
    for x in range(index//3+1) :
        number=number+4
        sequence.append(number)
        number=number+4
        sequence.append(number)
        number=number-1
        sequence.append(number)
    print(sequence[index])

get_number(1) # print 4
get_number(5) # print 15 
get_number(10) # print 25 
get_number(30) # print 70