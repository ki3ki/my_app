document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    
    if (!loginForm) {
        console.error('Login form not found');
        return;
    }

    loginForm.addEventListener('submit', async function(event) {
        event.preventDefault();
        
        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value;
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        try {
            const response = await fetch('/adminapp/admin-login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify({ username, password }),
                credentials: 'same-origin'
            });
            
            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('access', data.access);
                localStorage.setItem('refresh', data.refresh);
                localStorage.setItem('is_admin', data.is_admin);
                
                window.location.href = '/adminapp/dashboard/';
            } else {
                document.getElementById('error-message').textContent = 'Invalid username or password.';
                document.getElementById('error-message').style.display = 'block';
            }
        } catch (error) {
            console.error('Login error:', error);
            document.getElementById('error-message').textContent = 'An error occurred. Please try again.';
            document.getElementById('error-message').style.display = 'block';
        }
    });
});