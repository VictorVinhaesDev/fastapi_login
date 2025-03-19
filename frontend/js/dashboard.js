document.addEventListener('DOMContentLoaded', () => {
    const logoutButton = document.getElementById('logout-button');
    const userEmailSpan = document.getElementById('user-email');
    const userIdSpan = document.getElementById('user-id');
    
    // Preenche as informações do usuário
    const userEmail = localStorage.getItem('user_email');
    const userId = localStorage.getItem('user_id');
    
    if (userEmail) {
        userEmailSpan.textContent = userEmail;
    }
    
    if (userId) {
        userIdSpan.textContent = userId;
    }
    
    // Carrega informações adicionais do usuário da API
    async function loadUserData() {
        const userData = await getUserInfo();
        if (userData) {
            // Aqui você pode adicionar mais informações do usuário se necessário
            console.log('Dados do usuário carregados:', userData);
        }
    }
    
    // Configura o botão de logout
    logoutButton.addEventListener('click', () => {
        logout();
    });
    
    // Carrega informações do usuário
    loadUserData();
});