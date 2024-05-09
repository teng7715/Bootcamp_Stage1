from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
import mysql.connector

app=FastAPI()
app.mount("/static",StaticFiles(directory="static"),name="static")
templates=Jinja2Templates(directory="templates")
app.add_middleware(SessionMiddleware, secret_key="霹靂卡霹靂拉拉", max_age=None)


mydb=mysql.connector.connect(
    user="root",            
	password="123456787654321",
	host="localhost",       
	database="website"
)

mycursor=mydb.cursor()


@app.get("/",response_class=HTMLResponse)
async def read_home(request:Request):

    signed_in=request.session.get("SIGNED-IN", False)
    if signed_in:  #如果request.session是True,表示確實有登入過 1.直接導去會員頁
        return RedirectResponse("/member")
    else:          #如果request.session是False,沒有登入過 1.顯示首頁內容
        return templates.TemplateResponse(
        "home.html",{"request": request}) 


@app.post("/signup")
async def signup(request:Request,name:str=Form(),username:str=Form(),password:str=Form()):
    
    #姓名可以重複
    #帳號『不能重複』--->所以在資料庫設計時，雖然基本上參照上週作業的架構，但在usename的欄位多加上unique key
    #密碼可以重複

    request.session["SIGNED-IN"]=False #註冊帳號的流程不是登入，所以SIGNED-IN狀態保險起見設定為False

    mycursor.execute("select username from member")
    username_list=[username[0] for username in mycursor.fetchall()] #將資料表中，所有username的資料，透過迴圈放入陣列

    if username in username_list: 
        #如果使用者輸入的username跟資料庫裡的username重複 1.導到失敗頁
        return RedirectResponse("/error?message=此帳號名稱已被使用，請改設定其他名稱",status_code=303)

    else: 
        #如果使用者輸入的username沒有跟資料庫裡的username重複 1.將資料寫入資料庫 2.導回首頁
        mycursor.execute("insert into member (name,username,password) values (%s,%s,%s)",(name,username,password))
        mydb.commit()
        return RedirectResponse("/",status_code=303)


@app.post("/signin")
async def signin(request:Request,username:str=Form(),password:str=Form()):

    mycursor.execute("select username,password from member")
    username_password_dict={key:value for key,value in mycursor.fetchall()} #將每一組帳號密碼變成字典組合
   
    if username in username_password_dict and password == username_password_dict[username]: 
        #如果帳號和密碼都與資料庫某筆資料相符
            #1.將使用者姓名、使用者id提取出來後，寫入session中
            #2.將SIGNED-IN的狀態改為True
            #3.導到會員頁

        #將這登入帳號的使用者姓名資料從MySQL中取出
        mycursor.execute("select name from member where username=%s",(username,)) 
        name=mycursor.fetchone()                    

        #將這登入帳號的id資料從MySQL中取出
        mycursor.execute("select id from member where username=%s",(username,))
        id=mycursor.fetchone()                   

        request.session["name"]=name[0]
        request.session["id"]=id[0]
        request.session["SIGNED-IN"]=True

        return RedirectResponse("/member",status_code=303)
    else: 
        #如果輸入的帳號密碼錯誤或不存在 1.保險起見將SIGNED-IN的狀態改為False 2.導去錯誤頁面
        request.session["SIGNED-IN"]=False
        return RedirectResponse("/error?message=帳號或密碼輸入錯誤",status_code=303)


@app.get("/member",response_class=HTMLResponse)
async def open_success(request:Request):

    signed_in=request.session.get("SIGNED-IN", False)
    if signed_in:  #如果request.session是True,表示確實有登入過

        #1.將session中的name資料取出，作為變數 2.將留言人姓名、留言編號、留言內容取出 3.拿來透過模板引擎渲染會員頁面
        name=request.session["name"]

        mycursor.execute("select member.name, message.id, message.content from message inner join member on message.member_id=member.id order by message.time DESC")
        all_messages= mycursor.fetchall()

        return templates.TemplateResponse(
            "success.html",{"request":request,"name":name,"all_messages":all_messages}
        )
    
    else:  #如果request.session是False,表示沒登入，直接暴力導回首頁 
        return RedirectResponse("/") 


@app.post("/createMessage") 
async def create_message(request:Request,content:str=Form()):

    signed_in=request.session.get("SIGNED-IN", False) 

    if signed_in:
        member_id=request.session["id"] #使用者狀態資訊中，抓出使用者id
        mycursor.execute("insert into message (member_id,content) values (%s,%s)",(member_id,content))
        mydb.commit()

        return RedirectResponse("/member",status_code=303)
    
    else:  #如果request.session是False,表示沒登入，直接導回首頁 
        return RedirectResponse("/",status_code=303) 
    

@app.post("/deleteMessage") 
async def delete_message(request:Request,message_id:str=Form()):

    signed_in=request.session.get("SIGNED-IN", False)
    if signed_in:

        #從前端抓取member_id
        member_id=request.session["id"]
        
        #從前端獲得留言ID，並把他從字串轉換成整數數值
        message_id=int(message_id)

        #再次於後端檢查：要刪除的留言撰寫人，是否跟現在登入的人是同一個
        mycursor.execute("select member_id from message where id=%s",(message_id,))
        check_number=mycursor.fetchone()

        if member_id==check_number[0]: 
            mycursor.execute("delete from message where id=%s",(message_id,))
            mydb.commit()
            return RedirectResponse("/member",status_code=303)

    else:  
        return RedirectResponse("/",status_code=303) 
    

@app.get("/error",response_class=HTMLResponse)
async def open_error(request:Request,message:str):


    signed_in=request.session.get("SIGNED-IN", False)
    if not signed_in: #如果真的沒有登入過，就顯示失敗頁內容
        return templates.TemplateResponse(
        "error.html",{"request":request,"message":message}
    )
    else: #反之如果是登入後，以暴力網址的方式輸入，仍強制導回會員頁
        return RedirectResponse("/member")


@app.get("/signout")
async def signout(request:Request): 
    #點擊登出後，1.將登入狀態調整為False 2.刪除使用者狀態紀錄的使用者姓名資料  3.刪除使用者狀態紀錄的使用者id 4.導回首頁
    request.session["SIGNED-IN"]=False
    del request.session["name"]
    del request.session["id"]
    return RedirectResponse("/")