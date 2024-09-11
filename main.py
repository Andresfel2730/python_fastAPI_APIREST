# API REST: Interfaz de  programacion de aplicaciones para compartir recursos
from typing import List, Optional
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


# inicializamos una variable que tendra todas las caracteristicas de una API REST
app = FastAPI()

# Aca definimos el modelo
class Curso(BaseModel):
    id: Optional [str] = None
    nombre: str
    descripcion: Optional[str] = None
    nivel: str
    duracion: int
    
# simularemos una base de datos
cursos_db = []

# CRUD: read (lectura) GET ALL: Leeremos todos los cursos que haya en la db
@app.get("/cursos/", response_model=List[Curso])
def obtener_cursos():
    return cursos_db

# CRUD: Create (escribir) Post: agregamos un nuevo recurso a la base de datos
@app.post("/cursos/", response_model=Curso)
def crear_curso(curso:Curso):
    curso.id = str(uuid.uuid4()) # usamos un UUID para generar un ID unico e irrepetible
    cursos_db.append(curso)
    return curso

# CRUD: Read (lectura) GET (individual): leeremos el curso que coincida con el ID que pidamos
@app.get("/cursos/{curso_id}", response_model=Curso)
def obtener_curso(curso_id:str):
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None) # con next tomamos la primera coicidencia del array devuelto
    if curso is None:
        raise HTTPException(status_code=404, detail="curso no encontrado")
    return curso


#CRUD: update (actualizar/modificar) PUT: modificaremos un recurso que coincida con el ID que mandemos
@app.put("/cursos/{curso_id}",response_model=Curso)
def actualizar_curso(curso_id:str, curso_actualizado:Curso):
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None) # con next tomamos la primera coicidencia del array devuelto
    if curso is None:
        raise HTTPException(status_code=404, detail="curso no encontrado")
    curso_actualizado.id = curso_id
    index = cursos_db.index(curso) # buscamos el indice exacto donde esta el curso en nuestra lsta (DB)
    cursos_db[index] = curso_actualizado
    return curso_actualizado


# CRUD: DELETE (borrado/baja) DELETE: eliminaremos un recurso que coincida con ID que mandamos
@app.delete("/cursos/{curso_id}", response_model=Curso)
def eliminar_curso(curso_id:str):
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None) # con next tomamos la primera coicidencia del array devuelto
    if curso is None:
        raise HTTPException(status_code=404, detail="curso no encontrado")
    cursos_db.remove(curso)
    return curso
    
    

    
    
