from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles
from api.routes import router
from api import auth
from db.session import init
from fastapi.middleware.cors import CORSMiddleware
from api import routes, recepie
app = FastAPI(
    default_response_class=ORJSONResponse,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
)

app.mount("/templates", StaticFiles(directory="templates"), name="templates")

# Сначала добавляем CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Затем подключаем роутеры

app.include_router(routes.router, prefix='', tags=["main"]) # главная страница
app.include_router(auth.router,prefix='', tags=['auth'] )


# app.mount("/static", StaticFiles(directory="static"), name="static")


init()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
