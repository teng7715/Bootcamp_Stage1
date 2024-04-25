from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

app=FastAPI()

app.mount("/static",StaticFiles(directory="static"),name="static")
templates=Jinja2Templates(directory="templates")
app.add_middleware(SessionMiddleware, secret_key="霹靂卡霹靂拉拉", max_age=None)


@app.get("/",response_class=HTMLResponse) 
async def read_home(request:Request):

    signed_in=request.session.get("SIGNED-IN", False)  #判斷request.session裡面有沒有登入的資料，有的話拿出來，沒有的話，預設False
    if signed_in:  #如果request.session是True,就導他去登入成功頁面
        return RedirectResponse("/member/")
    else:
        return templates.TemplateResponse(
        "home.html",{"request": request}) 


@app.post("/signin")
async def signin(request:Request, username:str=Form(None), password:str=Form(None)):

    if not username or not password:
        return RedirectResponse("/error?message=請輸入帳號、密碼",status_code=303)

    if username=="test" and password=="test":
        request.session["SIGNED-IN"]=True
        return RedirectResponse("/member",status_code=303)
    else:
        return RedirectResponse("/error?message=帳號、或密碼輸入錯誤",status_code=303)


@app.get("/member",response_class=HTMLResponse) 
async def open_success(request:Request):
    signed_in=request.session.get("SIGNED-IN", False)  #判斷request.session裡面有沒有登入的資料，有的話拿出來，沒有的話，預設False
    if signed_in:  #如果request.session是True,就導他去登入成功頁面
        return templates.TemplateResponse(
            "success.html",{"request": request})
    else:
        return RedirectResponse("/") 


@app.get("/error",response_class=HTMLResponse)
async def open_error(request:Request,message:str):
    return templates.TemplateResponse(
        "error.html",{"request": request,"message": message})


@app.get("/signout",response_class=HTMLResponse) 
async def signout(request:Request):
    request.session["SIGNED-IN"]=False
    return RedirectResponse("/")