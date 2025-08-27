// URL del backend API
const API_URL = 'http://localhost:8000';

// Elementos del DOM
const feed = document.getElementById('feed');
const refreshBtn = document.getElementById('refreshBtn');

// Estado de la aplicación
let posts = [];
let loading = false;

// Inicializar la aplicación
document.addEventListener('DOMContentLoaded', () => {
    loadPosts();
    
    // Event listener para el botón de actualizar
    refreshBtn.addEventListener('click', () => {
        loadPosts();
    });
});

// Función para cargar posts desde el backend
async function loadPosts() {
    if (loading) return;
    
    loading = true;
    showLoading();
    
    try {
        const response = await fetch(`${API_URL}/posts`);
        
        if (!response.ok) {
            throw new Error('Error al cargar los posts');
        }
        
        posts = await response.json();
        renderPosts();
        
    } catch (error) {
        console.error('Error:', error);
        showError('No se pudieron cargar los posts. ¿Está funcionando el backend?');
    } finally {
        loading = false;
        refreshBtn.classList.remove('loading');
    }
}

// Mostrar estado de carga
function showLoading() {
    refreshBtn.classList.add('loading');
    feed.innerHTML = '<div class="loading">Cargando posts...</div>';
}

// Mostrar error
function showError(message) {
    feed.innerHTML = `<div class="error">${message}</div>`;
}

// Renderizar todos los posts
function renderPosts() {
    if (posts.length === 0) {
        feed.innerHTML = '<div class="loading">No hay posts disponibles</div>';
        return;
    }
    
    feed.innerHTML = '';
    
    posts.forEach((post, index) => {
        const postElement = createPostElement(post, index);
        feed.appendChild(postElement);
    });
}

// Crear elemento HTML para un post
function createPostElement(post, index) {
    const postDiv = document.createElement('div');
    postDiv.className = 'post';
    postDiv.style.animationDelay = `${index * 0.1}s`;
    
    postDiv.innerHTML = `
        <img src="${post.foto}" alt="Post image" class="post-image" onerror="this.src='https://via.placeholder.com/400x250/667eea/white?text=Imagen+no+disponible'">
        
        <div class="post-content">
            <div class="post-user">
                <div class="user-avatar">${post.usuario.charAt(0).toUpperCase()}</div>
                <div class="user-name">${post.usuario}</div>
            </div>
            
            <div class="post-description">${post.descripcion}</div>
            
            <div class="post-actions">
                <button class="action-btn like-btn" onclick="toggleLike(${post.id})">
                    <span class="like-icon">${post.megusta > 0 ? '❤️' : '🤍'}</span>
                    <span class="like-count">${post.megusta}</span>
                </button>
                
                <div class="comments-count">
                    💬 ${post.comentarios.length} comentarios
                </div>
                
                <button class="action-btn share-btn" onclick="sharePost(${post.id})">
                    📤 Compartir
                </button>
            </div>
        </div>
    `;
    
    return postDiv;
}

// Función para dar/quitar like (simulada)
function toggleLike(postId) {
    const post = posts.find(p => p.id === postId);
    if (post) {
        // Toggle like (simulado - en un app real esto sería una llamada al backend)
        if (post.megusta > 0) {
            post.megusta = 0;
        } else {
            post.megusta = 1;
        }
        
        // Re-renderizar posts
        renderPosts();
        
        // Animación simple
        const likeBtn = document.querySelector(`[onclick="toggleLike(${postId})"]`);
        if (likeBtn) {
            likeBtn.style.transform = 'scale(1.3)';
            setTimeout(() => {
                likeBtn.style.transform = 'scale(1)';
            }, 200);
        }
    }
}

// Función para compartir post (simulada)
function sharePost(postId) {
    const post = posts.find(p => p.id === postId);
    if (post) {
        // Simulamos compartir
        alert(`¡Compartiendo post de ${post.usuario}!`);
    }
}

// Manejar errores de imágenes
document.addEventListener('error', (e) => {
    if (e.target.tagName === 'IMG') {
        e.target.src = 'https://via.placeholder.com/400x250/667eea/white?text=Imagen+no+disponible';
    }
}, true);

// Smooth scroll para el feed
function scrollToTop() {
    feed.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Auto-refresh cada 30 segundos (opcional)
setInterval(() => {
    if (!loading) {
        loadPosts();
    }
}, 30000);
