document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const messageDiv = document.getElementById('login-message');
    
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Limpar mensagens anteriores
        messageDiv.textContent = '';
        messageDiv.className = 'message';
        
        // Obter valores do formulário
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        
        // Tenta fazer login
        const result = await login(email, password);
        
        if (result.success) {
            // Exibe mensagem de sucesso
            messageDiv.textContent = 'Login realizado com sucesso! Redirecionando...';
            messageDiv.classList.add('success');
            
            // Redireciona para a dashboard após um breve delay
            setTimeout(() => {
                window.location.href = 'dashboard.html';
            }, 1000);
        } else {
            // Exibe mensagem de erro
            messageDiv.textContent = result.message || 'Erro ao fazer login. Verifique suas credenciais.';
            messageDiv.classList.add('error');
        }
    });
});