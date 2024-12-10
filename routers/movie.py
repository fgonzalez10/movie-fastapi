from fastapi import  HTTPException, Path, Query, Request,Depends, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
from user_jwt import  validateToken
from fastapi.security import HTTPBearer
from bd.database import Session
from models.movie import Movie as ModelMovie
from fastapi.encoders import jsonable_encoder



routerMovie = APIRouter()

class BearerJWT(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validateToken(auth.credentials)
        if data['email'] != 'fgonzalez@notario.com.mx':
            raise HTTPException(status_code=403, detail='Credenciales incorrectas')

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(default='Titulo de la pelicula', min_length=5, max_length=60)
    overview: str = Field(default='Descripcion de la pelicula', min_length=15, max_length=150)
    year: int = Field(default=2024)
    rating: float = Field(ge=1, le=10)
    category: str = Field(default='Categoria' ,min_length=3, max_length=15)

    # def to_dict(self):
    #     return{
    #         "id": self.id,
    #         "title":self.title,
    #         "overview":self.overview,
    #         "year":self.year,
    #         "rating":self.rating,
    #         "category":self.category
    #     }





@routerMovie.get('/movies', tags=['Movies'], dependencies=[Depends(BearerJWT())])
def get_movies():
    db = Session()
    data = db.query(ModelMovie).all()
    return JSONResponse(content=jsonable_encoder(data))


@routerMovie.get('/movies/{id}', tags=['Movies'], status_code=200)
def get_movie(id: int = Path(ge=1, le=100)):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data :
        return JSONResponse(status_code=404, content={'message:': 'Recurso no encontrado'})
    return JSONResponse(status_code=200, content=jsonable_encoder(data))

@routerMovie.get('/movies/', tags=['Movies'])
def get_movies_by_category(category: str = Query(min_length=3, max_length=100)):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.category == category).all()
    if not data: 
        return JSONResponse(status_code=404, content={'message':'Recurso no encontrado'})
    return JSONResponse(status_code=200, content=jsonable_encoder(data))  


@routerMovie.post('/movies', tags=['Movies'], status_code=201)
def create_movie(movie: Movie):
    db = Session()
    newMovie = ModelMovie(**movie.dict())
    db.add(newMovie)
    db.commit()
    return JSONResponse(status_code=201,content={'message': 'Se ha cargado una nueva pelicula'})

@routerMovie.put('/movies/{id}', tags=['Movies'], status_code=200)
def update_movie(id:int, movie: Movie):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data :
        return JSONResponse(status_code=404, content={'message:': 'Recurso no encontrado'})
    data.title = movie.title
    data.overview = movie.overview
    data.year = movie.year
    data.rating = movie.rating
    data.category = movie.category
    db.commit()
    return JSONResponse(content={'message: ': 'Se ha modificado la pelicula'})
    
           
    

@routerMovie.delete('/movies/{id}', tags=['Movies'], status_code=200)
def delete_movie(id:int):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data :
        return JSONResponse(status_code=404, content={'message:': 'Recurso no encontrado'})
    db.delete(data)
    db.commit()
    return JSONResponse(content={'message:':'Se ha eliminado una pelicula'})    