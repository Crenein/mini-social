from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
from pydantic import BaseModel
import json
import os

# Crear la aplicación FastAPI
app = FastAPI(title="Mini Social API", description="API simple para el feed de Mini Social")

# Archivo JSON para persistir los posts
POSTS_FILE = "posts.json"

# Modelo para crear nuevos posts
class NewPost(BaseModel):
    username: str
    image: str
    description: str

# Funciones para manejar el archivo JSON
def load_posts():
    """Carga los posts desde el archivo JSON"""
    if os.path.exists(POSTS_FILE):
        try:
            with open(POSTS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    return []

def save_posts(posts):
    """Guarda los posts en el archivo JSON"""
    with open(POSTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

def get_next_id(posts):
    """Obtiene el siguiente ID disponible"""
    if not posts:
        return 1
    return max(post['id'] for post in posts) + 1

def find_post_by_id(posts, post_id):
    """Encuentra un post por su ID"""
    for post in posts:
        if post['id'] == post_id:
            return post
    return None

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
        "description": "API simple para el feed de posts"        
    }

@app.get("/posts", response_model=List[Dict[str, Any]])
async def get_posts():
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
    posts = load_posts()
    # Ordenar por ID descendente (más recientes primero)
    posts.sort(key=lambda x: x['id'], reverse=True)
    return posts

@app.get("/posts/{post_id}")
async def get_post(post_id: int):
    """Obtener un post específico por ID"""
    posts = load_posts()
    post = find_post_by_id(posts, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post no encontrado")
    return post

@app.post("/posts")
async def create_post(new_post: NewPost):
    """Crear un nuevo post"""
    posts = load_posts()
    
    # Crear el nuevo post
    post = {
        "id": get_next_id(posts),
        "username": new_post.username,
        "image": new_post.image,
        "description": new_post.description,
        "comments": [],  # Lista vacía de comentarios
        "likes": 0
    }
    
    posts.append(post)
    save_posts(posts)
    
    return post

@app.post("/posts/{post_id}/like")
async def like_post(post_id: int):
    """Dar like a un post"""
    posts = load_posts()
    post = find_post_by_id(posts, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post no encontrado")
    
    post['likes'] += 1
    save_posts(posts)
    return {"message": "Like agregado", "likes": post['likes']}

@app.delete("/posts/{post_id}/like")
async def unlike_post(post_id: int):
    """Quitar like a un post"""
    posts = load_posts()
    post = find_post_by_id(posts, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post no encontrado")
    
    if post['likes'] > 0:
        post['likes'] -= 1
    save_posts(posts)
    return {"message": "Like removido", "likes": post['likes']}

@app.delete("/posts/{post_id}")
async def delete_post(post_id: int):
    """Eliminar un post por ID"""
    posts = load_posts()
    post = find_post_by_id(posts, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post no encontrado")
    
    posts = [p for p in posts if p['id'] != post_id]
    save_posts(posts)
    return {"message": "Post eliminado correctamente", "id": post_id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
