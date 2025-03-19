document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.getElementById('register-form');
    const messageDiv = document.getElementById('register-message');
    
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Limpar mensagens anteriores
        messageDiv.textContent = '';
        messageDiv.className = 'message';
        
        // Obter valores do formulário
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        
        // Validação simples da senha
        if (password.length < 6) {
            messageDiv.textContent = 'A senha deve ter pelo menos 6 caracteres';
            messageDiv.classList.add('error');
            return;
        }
        
        // Tenta registrar o usuário
        const result = await register(email, password);
        
        if (result.success) {
            // Exibe mensagem de sucesso
            messageDiv.textContent = 'Cadastro realizado com sucesso! Redirecionando para o login...';
            messageDiv.classList.add('success');
            
            // Redireciona para a página de login após um breve delay
            setTimeout(() => {
                window.location.href = 'index.html';
            }, 2000);
        } else {
            // Exibe mensagem de erro
            messageDiv.textContent = result.message || 'Erro ao criar conta. Tente novamente.';
            messageDiv.classList.add('error');
        }
    });
});