# Mini Social - Configuración del Entorno

## Requisitos previos
- Python 3.7 o superior
- pip (gestor de paquetes de Python)

## Configuración del Entorno Virtual

### En Linux/macOS

1. **Crear entorno virtual:**
   ```bash
   python3 -m venv .venv
   ```

2. **Activar entorno virtual:**
   ```bash
   source .venv/bin/activate
   ```

3. **Desactivar entorno virtual:**
   ```bash
   deactivate
   ```

### En Windows

1. **Crear entorno virtual:**
   ```cmd
   python -m venv .venv
   ```

2. **Activar entorno virtual:**
   ```cmd
   .venv\Scripts\activate
   ```

3. **Desactivar entorno virtual:**
   ```cmd
   deactivate
   ```

## Instalación de Dependencias

Una vez activado el entorno virtual, instala las dependencias del proyecto:

```bash
cd backend
pip install -r requirements.txt
```

## Ejecutar el Proyecto

### Backend (FastAPI)
```bash
cd backend
uvicorn main:app --reload
```

# documentacion de API
http://127.0.0.1:8000/docs

### Frontend
Abre el archivo `frontend/index.html` en tu navegador web.

## Estructura del Proyecto

```
mini-social/
├── backend/
│   ├── main.py
│   └── requirements.txt
└── frontend/
    ├── index.html
    ├── script.js
    └── style.css
```

## Dependencias Actuales

- **FastAPI 0.104.1**: Framework web para crear APIs
- **Uvicorn 0.24.0**: Servidor ASGI para ejecutar FastAPI



# APIs interesantes

https://medium.com/@diego.coder/las-mejores-apis-p%C3%BAblicas-para-practicar-programaci%C3%B3n-a7419ecc968e


# preprar entorno window 

- bajar proyecto
- instalar vscode
- instalar python (habiltar el agregado al PATH)
- en vscode:
- - instalar extension python
- - seleccionar interprete de python 
- - crear entorno virtual (capas no haga falta)
- - select requirements.txt (capas no haga falta)
- - ejecutar main.py desde vscode
- - en 0.0.0.0 no funca se usa localhost:8000/docs

