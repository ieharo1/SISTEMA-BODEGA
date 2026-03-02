from datetime import timedelta
from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.schemas.schemas import UserCreate, UserLogin, Token
from app.services.auth_service import create_access_token
from app.repositories.repository import repository
from app.config import settings

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/login", name="login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login", name="login_post")
async def login(request: Request, credentials: UserLogin):
    user = await repository.authenticate_user(credentials.email, credentials.password)
    if not user:
        return templates.TemplateResponse(
            "login.html", {"request": request, "error": "Credenciales inválidas"}
        )

    access_token = create_access_token(
        data={"sub": user["email"], "user_id": user["id"]},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    response = RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response


@router.get("/register", name="register")
async def register_page(request: Request):
    return templates.TemplateResponse(
        "login.html", {"request": request, "register_mode": True}
    )


@router.post("/register", name="register_post")
async def register(request: Request, user_data: UserCreate):
    existing_user = await repository.get_user_by_email(user_data.email)
    if existing_user:
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "register_mode": True,
                "error": "El email ya está registrado",
            },
        )

    user = await repository.create_user(user_data)
    access_token = create_access_token(
        data={"sub": user["email"], "user_id": user["id"]},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    response = RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response


@router.get("/logout", name="logout")
async def logout():
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("access_token")
    return response
