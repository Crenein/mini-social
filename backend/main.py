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
        "usuario": "Ana García",
        "foto": "https://picsum.photos/400/250?random=1",
        "descripcion": "¡Hermoso atardecer en la playa! 🌅 Un día perfecto para relajarse.",
        "comentarios": [
            {"usuario": "Carlos", "texto": "¡Qué hermosa vista!"},
            {"usuario": "María", "texto": "Me encanta esa playa"}
        ],
        "megusta": 15
    },
    {
        "id": 2,
        "usuario": "Luis Martín",
        "foto": "https://picsum.photos/400/250?random=2",
        "descripcion": "Nuevo proyecto de programación terminado 💻 ¡Aprendiendo cada día más!",
        "comentarios": [
            {"usuario": "Elena", "texto": "¡Felicidades!"},
            {"usuario": "Pedro", "texto": "¿Qué tecnologías usaste?"},
            {"usuario": "Ana García", "texto": "Muy inspirador"}
        ],
        "megusta": 23
    },
    {
        "id": 3,
        "usuario": "Sofia Chen",
        "foto": "https://picsum.photos/400/250?random=3",
        "descripcion": "Deliciosa cena casera 🍝 Nada como cocinar con amor para la familia.",
        "comentarios": [
            {"usuario": "Roberto", "texto": "Se ve delicioso!"}
        ],
        "megusta": 8
    },
    {
        "id": 4,
        "usuario": "Miguel Torres",
        "foto": "https://picsum.photos/400/250?random=4",
        "descripción": "Entrenamiento matutino en el parque 🏃‍♂️ ¡La energía para todo el día!",
        "comentarios": [
            {"usuario": "Laura", "texto": "¡Qué disciplina!"},
            {"usuario": "Carlos", "texto": "Me motivas a hacer ejercicio"}
        ],
        "megusta": 12
    },
    {
        "id": 5,
        "usuario": "Emma Wilson",
        "foto": "https://picsum.photos/400/250?random=5",
        "descripcion": "Nuevo libro terminado 📚 Recomiendo mucho esta novela de ciencia ficción.",
        "comentarios": [
            {"usuario": "David", "texto": "¿Cuál es el título?"},
            {"usuario": "Sofia Chen", "texto": "Me gusta la ciencia ficción"}
        ],
        "megusta": 18
    },
    {
        "id": 6,
        "usuario": "Roberto Silva",
        "foto": "https://picsum.photos/400/250?random=6",
        "descripcion": "Concierto increíble anoche 🎵 La música en vivo no tiene comparación.",
        "comentarios": [],
        "megusta": 5
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
