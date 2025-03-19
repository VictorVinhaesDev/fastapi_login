// Configuração da API
const API_URL = 'http://localhost:8000'; // Ajuste conforme a URL do seu backend

// Função para verificar se o usuário está autenticado
function isAuthenticated() {
    return localStorage.getItem('token') !== null;
}

// Função para verificar a autenticação e redirecionar se necessário
function checkAuth(requiredAuth = true) {
    const isAuth = isAuthenticated();
    const currentPath = window.location.pathname;
    
    // Se estiver autenticado e tentar acessar páginas de login/registro
    if (isAuth && (currentPath.includes('index.html') || currentPath.includes('register.html') || currentPath === '/')) {
        window.location.href = 'dashboard.html';
        return;
    }
    
    // Se não estiver autenticado e tentar acessar páginas protegidas
    if (!isAuth && requiredAuth && currentPath.includes('dashboard.html')) {
        window.location.href = 'index.html';
        return;
    }
}

// Função para fazer login
async function login(email, password) {
    try {
        const response = await fetch(`${API_URL}/token`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                'username': email, // FastAPI usa 'username' para login com email por padrão
                'password': password
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Falha ao fazer login');
        }
        
        // Guarda o token e informações do usuário
        localStorage.setItem('token', data.access_token);
        localStorage.setItem('user_id', data.user_id);
        localStorage.setItem('user_email', email);
        
        return { success: true };
    } catch (error) {
        return { success: false, message: error.message };
    }
}

// Função para registrar um novo usuário
async function register(email, password) {
    try {
        const response = await fetch(`${API_URL}/users/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email,
                password
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Falha ao registrar usuário');
        }
        
        return { success: true };
    } catch (error) {
        return { success: false, message: error.message };
    }
}

// Função para fazer logout
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user_id');
    localStorage.removeItem('user_email');
    window.location.href = 'index.html';
}

// Função para obter informações do usuário
async function getUserInfo() {
    const token = localStorage.getItem('token');
    const userId = localStorage.getItem('user_id');
    
    if (!token || !userId) {
        return null;
    }
    
    try {
        const response = await fetch(`${API_URL}/users/${userId}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            throw new Error('Falha ao obter informações do usuário');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Erro ao obter informações do usuário:', error);
        return null;
    }
}

// Verificar autenticação ao carregar a página
document.addEventListener('DOMContentLoaded', () => {
    // Determina se a página atual requer autenticação
    const currentPath = window.location.pathname;
    const requiresAuth = currentPath.includes('dashboard.html');
    
    checkAuth(requiresAuth);
});