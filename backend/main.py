from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text, JSON
from sqlalchemy.orm import sessionmaker, Session, declarative_base
import json

# Crear la aplicación FastAPI
app = FastAPI(title="Mini Social API", description="API simple para el feed de Mini Social")

# Configuración de la base de datos SQLite
DATABASE_URL = "sqlite:///./posts.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo de base de datos para los posts
class PostDB(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    image = Column(String)
    description = Column(Text)
    comments = Column(Text)  # Almacenar como JSON string
    likes = Column(Integer, default=0)

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Modelo para crear nuevos posts
class NewPost(BaseModel):
    username: str
    image: str
    description: str

# Funciones auxiliares para la conversión de datos
def post_db_to_dict(post_db: PostDB) -> dict:
    """Convierte un objeto PostDB a diccionario"""
    return {
        "id": post_db.id,
        "username": post_db.username,
        "image": post_db.image,
        "description": post_db.description,
        "comments": json.loads(post_db.comments) if post_db.comments else [],
        "likes": post_db.likes
    }

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Función para inicializar datos predefinidos
def init_database():
    """Inicializa la base de datos con datos predefinidos si está vacía"""
    db = SessionLocal()
    try:
        # Verificar si ya hay posts en la base de datos
        existing_posts = db.query(PostDB).first()
        if existing_posts is None:
            # Datos predefinidos de posts
            initial_posts = [
                {
                    "id": 1,
                    "username": "Ana García",
                    "image": "https://fastly.picsum.photos/id/12/400/250.jpg?hmac=lRVx-FWXSB1f69BtdBwcL5mJ1pKf8obBCBPVpl-Ov3M",
                    "description": "¡Hermoso atardecer en la playa! 🌅 Un día perfecto para relajarse.",
                    "comments": [
                        {"username": "Carlos", "text": "¡Qué hermosa vista!"},
                        {"username": "María", "text": "Me encanta esa playa"}
                    ],
                    "likes": 15
                },
                {
                    "id": 2,
                    "username": "Luis Martín",
                    "image": "https://fastly.picsum.photos/id/9/400/250.jpg?hmac=UEfGO3_VQdnRPR53mZz4Rx5NV-dtW__WJDeaqc-c2aw",
                    "description": "Nuevo proyecto de programación terminado 💻 ¡Aprendiendo cada día más!",
                    "comments": [
                        {"username": "Elena", "text": "¡Felicidades!"},
                        {"username": "Pedro", "text": "¿Qué tecnologías usaste?"},
                        {"username": "Ana García", "text": "Muy inspirador"}
                    ],
                    "likes": 23
                },
                {
                    "id": 3,
                    "username": "Sofia Chen",
                    "image": "https://fastly.picsum.photos/id/250/400/250.jpg?hmac=5wN2lOf0VLAk18B1cnw4PyqLBjk2eGsqJW_SuQKaHQc",
                    "description": "¡Compré una cámara de fotos nueva y estoy súper feliz! 📸 Ya quiero salir a capturar momentos increíbles.",
                    "comments": [
                        {"username": "Roberto", "text": "¡Qué emocionante! ¿Qué modelo compraste?"}
                    ],
                    "likes": 8
                },
                {
                    "id": 4,
                    "username": "Miguel Torres",
                    "image": "https://fastly.picsum.photos/id/237/400/250.jpg?hmac=PePeCqT_HNK24hBSuOnnbpe3Bmq-6n32sj8FJRHhpHY",
                    "description": "¡Conoce a mi nueva mascota! 🐕 Este pequeño perrito ya se ha robado mi corazón. ¡La vida es mucho mejor con una mascota fiel!",
                    "comments": [
                        {"username": "Laura", "text": "¡Qué hermoso! ¿Cómo se llama?"},
                        {"username": "Carlos", "text": "Los perros son los mejores compañeros"}
                    ],
                    "likes": 12
                }
            ]
            
            # Insertar los posts iniciales
            for post_data in initial_posts:
                post_db = PostDB(
                    username=post_data["username"],
                    image=post_data["image"],
                    description=post_data["description"],
                    comments=json.dumps(post_data["comments"]),
                    likes=post_data["likes"]
                )
                db.add(post_db)
            db.commit()
    finally:
        db.close()

# Inicializar la base de datos
init_database()

# Configurar CORS para permitir conexiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica el dominio del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Endpoint raíz con información de la API"""
    return {
        "message": "Mini Social API",
        "description": "API simple para el feed de posts",
        "endpoints": {
            "/posts": "GET - Obtener todos los posts, POST - Crear nuevo post",
            "/posts/{id}": "GET - Obtener post específico, DELETE - Eliminar post",
            "/posts/{id}/like": "POST - Dar like, DELETE - Quitar like",
            "/docs": "Documentación interactiva de la API"
        }
    }

@app.get("/posts", response_model=List[Dict[str, Any]])
async def get_posts(db: Session = Depends(get_db)):
    """
    Obtener todos los posts del feed
    
    Retorna una lista de posts con:
    - id: identificador único
    - usuario: nombre del usuario
    - foto: URL de la imagen
    - descripcion: texto descriptivo del post
    - comentarios: lista de comentarios
    - megusta: cantidad de likes
    """
    posts = db.query(PostDB).order_by(PostDB.id.desc()).all()
    return [post_db_to_dict(post) for post in posts]

@app.get("/posts/{post_id}")
async def get_post(post_id: int, db: Session = Depends(get_db)):
    """Obtener un post específico por ID"""
    post = db.query(PostDB).filter(PostDB.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post no encontrado")
    return post_db_to_dict(post)

@app.post("/posts")
async def create_post(new_post: NewPost, db: Session = Depends(get_db)):
    """Crear un nuevo post"""
    # Crear el nuevo post en la base de datos
    post_db = PostDB(
        username=new_post.username,
        image=new_post.image,
        description=new_post.description,
        comments=json.dumps([]),  # Lista vacía de comentarios
        likes=0
    )
    
    db.add(post_db)
    db.commit()
    db.refresh(post_db)
    
    return post_db_to_dict(post_db)

@app.post("/posts/{post_id}/like")
async def like_post(post_id: int, db: Session = Depends(get_db)):
    """Dar like a un post"""
    post = db.query(PostDB).filter(PostDB.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post no encontrado")
    
    post.likes += 1
    db.commit()
    return {"message": "Like agregado", "likes": post.likes}

@app.delete("/posts/{post_id}/like")
async def unlike_post(post_id: int, db: Session = Depends(get_db)):
    """Quitar like a un post"""
    post = db.query(PostDB).filter(PostDB.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post no encontrado")
    
    if post.likes > 0:
        post.likes -= 1
    db.commit()
    return {"message": "Like removido", "likes": post.likes}

@app.delete("/posts/{post_id}")
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    """Eliminar un post por ID"""
    post = db.query(PostDB).filter(PostDB.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post no encontrado")
    
    db.delete(post)
    db.commit()
    return {"message": "Post eliminado correctamente", "id": post_id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
