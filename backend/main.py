from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any

# Crear la aplicación FastAPI
app = FastAPI(title="Mini Social API", description="API simple para el feed de Mini Social")

# Configurar CORS para permitir conexiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica el dominio del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Datos predefinidos de posts
posts_data = [
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

@app.get("/")
async def root():
    """Endpoint raíz con información de la API"""
    return {
        "message": "Mini Social API",
        "description": "API simple para el feed de posts",
        "endpoints": {
            "/posts": "GET - Obtener todos los posts",
            "/docs": "Documentación interactiva de la API"
        }
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
    return posts_data

@app.get("/posts/{post_id}")
async def get_post(post_id: int):
    """Obtener un post específico por ID"""
    for post in posts_data:
        if post["id"] == post_id:
            return post
    return {"error": "Post no encontrado"}, 404

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
