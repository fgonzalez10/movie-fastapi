from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from bd.database import engine, Base
from routers.movie import routerMovie
from routers.user import login_user
import uvicorn
import os






app = FastAPI(
    title='Aprendiendo FastAPI',
    description='Una api en los primeros pasos',
    version='0.0.1'
)

app.include_router(routerMovie)
app.include_router(login_user)

Base.metadata.create_all(bind=engine)





@app.get('/', tags=['inicio'])
def read_root():
    return HTMLResponse('<h2>Hola Mundo! </h2>')



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)