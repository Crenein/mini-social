// URL del backend API
const API_URL = 'http://localhost:8000';

// Elementos del DOM
const feed = document.getElementById('feed');
const refreshBtn = document.getElementById('refreshBtn');
const newPostBtn = document.getElementById('newPostBtn');
const newPostForm = document.getElementById('newPostForm');
const cancelBtn = document.getElementById('cancelBtn');
const submitBtn = document.getElementById('submitBtn');
const usernameInput = document.getElementById('usernameInput');
const imageInput = document.getElementById('imageInput');
const descriptionInput = document.getElementById('descriptionInput');

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
    
    // Event listeners para el formulario de nuevo post
    newPostBtn.addEventListener('click', () => {
        showNewPostForm();
    });
    
    cancelBtn.addEventListener('click', () => {
        hideNewPostForm();
    });
    
    submitBtn.addEventListener('click', () => {
        createPost();
    });
    
    // Cerrar formulario al hacer click fuera
    newPostForm.addEventListener('click', (e) => {
        if (e.target === newPostForm) {
            hideNewPostForm();
        }
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
        <img src="${post.image}" alt="Post image" class="post-image">

        <div class="post-content">
            <div class="post-user">
                <div class="user-avatar">${post.username.charAt(0).toUpperCase()}</div>
                <div class="user-name">${post.username}</div>
            </div>

            <div class="post-description">${post.description}</div>

            <div class="post-actions">
                <button class="action-btn like-btn" onclick="toggleLike(${post.id})">
                    <span class="like-icon">${post.likes > 0 ? '❤️' : '🤍'}</span>
                    <span class="like-count">${post.likes}</span>
                </button>
                
                <div class="comments-count">
                    💬 ${post.comments.length} comentarios
                </div>
                
                <button class="action-btn share-btn" onclick="sharePost(${post.id})">
                    📤 Compartir
                </button>
            </div>
        </div>
    `;
    
    return postDiv;
}

// Función para dar/quitar like conectada al backend
async function toggleLike(postId) {
    const post = posts.find(p => p.id === postId);
    if (!post) return;
    
    try {
        let response;
        // Si ya tiene likes, quitar like, sino dar like
        if (post.likes > 0) {
            response = await fetch(`${API_URL}/posts/${postId}/like`, {
                method: 'DELETE'
            });
        } else {
            response = await fetch(`${API_URL}/posts/${postId}/like`, {
                method: 'POST'
            });
        }
        
        if (response.ok) {
            const result = await response.json();
            // Actualizar el post local
            post.likes = result.likes;
            
            // Actualizar solo el botón específico en lugar de re-renderizar todo
            updateLikeButton(postId, result.likes);
       
        }
    } catch (error) {
        console.error('Error al dar/quitar like:', error);
    }
}

// Función para actualizar solo el botón de like específico
function updateLikeButton(postId, newLikesCount) {
    // Encontrar el botón de like específico usando el postId
    const likeButtons = document.querySelectorAll('.like-btn');
    
    likeButtons.forEach(button => {
        // Verificar si este botón corresponde al post correcto
        const onclickAttr = button.getAttribute('onclick');
        if (onclickAttr && onclickAttr.includes(`toggleLike(${postId})`)) {
            // Actualizar el ícono
            const likeIcon = button.querySelector('.like-icon');
            const likeCount = button.querySelector('.like-count');
            
            if (likeIcon && likeCount) {
                likeIcon.textContent = newLikesCount > 0 ? '❤️' : '🤍';
                likeCount.textContent = newLikesCount;
            }
        }
    });
}

// Función para compartir post (simulada)
function sharePost(postId) {
    const post = posts.find(p => p.id === postId);
    if (post) {
        // Simulamos compartir
        alert(`¡Compartiendo post de ${post.username}!`);
    }
}

// Mostrar formulario de nuevo post
function showNewPostForm() {
    newPostForm.classList.remove('hidden');
    usernameInput.focus();
}

// Ocultar formulario de nuevo post
function hideNewPostForm() {
    newPostForm.classList.add('hidden');
    // Limpiar campos
    usernameInput.value = '';
    imageInput.value = '';
    descriptionInput.value = '';
}

// Crear nuevo post
async function createPost() {
    const username = usernameInput.value.trim();
    const image = imageInput.value.trim();
    const description = descriptionInput.value.trim();
    
    // Validación simple
    if (!username || !image || !description) {
        alert('Por favor completa todos los campos');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/posts`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                image: image,
                description: description
            })
        });
        
        if (response.ok) {
            const newPost = await response.json();
            // Agregar el nuevo post al inicio de la lista local
            posts.unshift(newPost);
            // Re-renderizar posts
            renderPosts();
            // Ocultar formulario
            hideNewPostForm();
            // Mensaje de éxito
            alert('¡Post creado exitosamente!');
        } else {
            throw new Error('Error al crear el post');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error al crear el post. Intenta de nuevo.');
    }
}



// Smooth scroll para el feed
function scrollToTop() {
    feed.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}