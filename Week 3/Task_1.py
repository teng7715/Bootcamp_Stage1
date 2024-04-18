import json
import urllib.request as request
import re
import csv

src1="https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1"
src2="https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2"


with request.urlopen(src1) as response1:
         data1=json.load(response1)  


with request.urlopen(src2) as response2:
         data2=json.load(response2) 


tourist_spots=data1["data"]["results"] #縮短data1取用時的資料長度
station=data2["data"] #縮短data2取用時的資料長度


#此迴圈的功用:將每個捷運站的地址，這個字串，按照空格做切割+擷取XX區的字串後，取代原本的資料 EX:'address': '內湖區'
for i in range(len(station)): 
    station[i]["address"]=station[i]["address"].split()[1][0:3]


#此迴圈的功用:將每個景點的所在的捷運站撈出來，組成陣列
for i in range(len(tourist_spots)): 
    for x in range(len(station)):
        if(tourist_spots[i]["SERIAL_NO"]==station[x]["SERIAL_NO"]): 
            tourist_spots[i]["SERIAL_NO"]=station[x]["MRT"] 
            tourist_spots[i]["district"]=station[x]["address"] 



rule=re.compile(r'(https?://\S+?\.(?:jpg|jpeg|png|gif))',re.I) #正則表達式的條件

#此迴圈功能:將每個景點的亂七八糟URL字串，都去跑正則表達式比對，並將比對後的結果回寫回去
for i in range(len(tourist_spots)): 
    string=tourist_spots[i]["filelist"]
    mo=rule.findall(string)  #mo這變數是串列的格式，內容就是我們找出來的圖片URL
    tourist_spots[i]["filelist"]=mo


# 將資料寫入csv，誕生spot.csv檔案
with open("spot.csv",mode="w",newline="",encoding="utf-8-sig")as file: 
    writer=csv.writer(file)
    for i in range(len(tourist_spots)):
        writer.writerow([tourist_spots[i]["stitle"],tourist_spots[i]["district"],tourist_spots[i]["longitude"],tourist_spots[i]["latitude"],tourist_spots[i]["filelist"][0]])
        

# 此迴圈功能:將景點與捷運站對應後，產出匯總所有捷運站對應到的景點列表
mrt_tourist_spot_all=[]

for i in range(len(station)):
    mrt=station[i]["MRT"]
    sublist=[mrt]
    for x in range(len(tourist_spots)):
        if tourist_spots[x]["SERIAL_NO"]==mrt: #翻譯：如果這個景點所在的捷運站，跟迴圈正在跑的捷運站一致...
            sublist.append(tourist_spots[x]["stitle"]) #翻譯：在這個站專屬的串列當中，寫入這個景點的名稱
    mrt_tourist_spot_all.append(sublist) #翻譯：上面「每個景點」的所屬站牌對照「某一站」的迴圈結束後，將這個站的專屬串列寫入總結果串列當中，之後再跑下一個站牌重新開始回圈


# 將資料寫入csv，誕生mrt.csv檔案
with open("mrt.csv",mode="w",newline="",encoding="utf-8-sig")as file:
    writer=csv.writer(file)
    for i in mrt_tourist_spot_all:
        writer.writerow(i)
