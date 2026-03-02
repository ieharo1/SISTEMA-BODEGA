from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.database import connect_to_mongodb, close_mongodb_connection
from app.routes import auth, warehouse


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongodb()
    yield
    await close_mongodb_connection()


app = FastAPI(
    title="Sistema de Bodega - FastAPI",
    description="Sistema de gestión de almacén",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(auth.router)
app.include_router(warehouse.router)


@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}
