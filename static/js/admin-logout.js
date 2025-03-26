document.addEventListener('DOMContentLoaded', function () {
    const logoutLink = document.getElementById('logout-link');

    if (!logoutLink) {
        console.error('Logout link not found');
        return;
    }

    logoutLink.addEventListener('click', async function (event) {
        event.preventDefault();

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

        try {
            // Send logout request to backend
            const response = await fetch('/api/auth/token/logout/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    ...(csrfToken && { 'X-CSRFToken': csrfToken }),
                },
                credentials: 'same-origin',
            });

            if (response.ok) {
                // Clear tokens and admin flag from local storage
                localStorage.removeItem('access');
                localStorage.removeItem('refresh');
                localStorage.removeItem('is_admin');

                // Redirect to admin login page
                window.location.href = '/adminapp/login/';
            } else {
                console.error('Logout failed');
                alert('Failed to log out. Please try again.');
            }
        } catch (error) {
            console.error('Logout error:', error);
            alert('An error occurred during logout. Please try again.');
        }
    });
});
