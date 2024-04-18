import urllib.request as req
import csv

result=[] 

#此函式功能：印出某一頁的所有討論標題，並將下一頁的網址傳出
def get_ptt_data(url): 

    #建立一個Request物件(是urllib.request當中的一個物件），附加Request Headers的資訊
    request=req.Request(url,headers={
        "Cookie":"over18=1",
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        })


    with req.urlopen(request) as response:
        data=response.read().decode("utf-8")


    import bs4   
    root=bs4.BeautifulSoup(data,"html.parser") 
    

    titles=root.find_all("div",class_="title") #尋找「所有」class="title"的div標籤
    like_dislike_counts=root.find_all("div",class_="nrec") #尋找文章推推數的標籤
    

    combine=list(zip(titles,like_dislike_counts))

    #此迴圈目的：以判斷文章是否刪除為主軸，去抓出每篇文章的標題、推推數、
    for title,count in combine:
        article_information=[]
        if title.a != None:       #如果標題包含a標籤（即文章沒有被刪除），就執行加入串列的動作
            article_information.append(title.a.string)
        else:                     #反之如果這標題沒有a標籤（即文章被刪除了），就強制跳到下一圈
            continue
        if count.span != None:    #如果他有推推數，就將他的推推文字寫入陣列
            article_information.append(count.span.string)
        else:                     #反之如果他沒有推推數，我們就給他一個文字0
            article_information.append("0")
        
        #此函式功用：專門開啟迴圈正在跑的文章，並去爬發文時間
        def get_article_time(url):
            try: #為了避免某一頁因為沒有發文時間，所以找不到的狀況發生，這裡需要用try跟except，避免Error後跑不動
                request=req.Request(url,headers={
                "Cookie":"over18=1",
                "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
                })

                with req.urlopen(request) as response:
                    data=response.read().decode("utf-8")

                import bs4
                root=bs4.BeautifulSoup(data,"html.parser") 

                
                time_tag=root.find("span",class_="article-meta-tag",string="時間")
                time_info=time_tag.find_next_sibling("span",class_="article-meta-value").string
                return time_info

            except:
                return ""
            
        time=get_article_time("https://www.ptt.cc"+title.a["href"])
        article_information.append(time)

        result.append(article_information)


    nextLine=root.find("a",string="‹ 上頁")
    return (nextLine["href"]) 
  

ptt_url="https://www.ptt.cc/bbs/Lottery/index.html"

page=0
while page<3:
    ptt_url="https://www.ptt.cc"+get_ptt_data(ptt_url) 
    page+=1


# 將資料寫入csv，誕生mrt.csv檔案
with open("article.csv",mode="w",newline="",encoding="utf-8-sig")as file:
    writer=csv.writer(file)
    for article in result:
        writer.writerow(article)
