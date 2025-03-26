// Check token expiration
function isTokenExpired(token) {
    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        return payload.exp < Math.floor(Date.now() / 1000);
    } catch {
        return true;
    }
}

// Fetch data with authentication
async function fetchWithAuth(url) {
    const token = localStorage.getItem('access');
    
    try {
        const response = await fetch(url, {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            }
        });

        if (!response.ok) {
            throw new Error('API request failed');
        }

        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        return null;
    }
}

// Initialize dashboard
document.addEventListener('DOMContentLoaded', async () => {
    const token = localStorage.getItem('access');
    const isAdmin = localStorage.getItem('is_admin');

    if (!token || !isAdmin || isTokenExpired(token)) {
        window.location.href = '/adminapp/login/';
        return;
    }

    const appListContainer = document.querySelector('.app-list-container');
    if (!appListContainer) return;

    appListContainer.innerHTML = `
        <div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
    `;

    const appsData = await fetchWithAuth('/userapp/api/apps/');

    if (appsData && appsData.apps && appsData.apps.length > 0) {
        let appCardsHTML = '';
        appsData.apps.forEach(app => {
            appCardsHTML += `
                <div class="card">
                    <div class="card-body d-flex justify-content-between align-items-center">
                        <div class="d-flex align-items-center">
                            <img src="${app.icon_url || '/static/default-icon.png'}" alt="${app.name}" class="app-icon">
                            <div class="app-details">
                                <h5>${app.name}</h5>
                                <small class="view-detail">${app.points} POINTS</small>
                            </div>
                        </div>
                        <a href="/adminapp/app/${app.id}/" class="btn btn-primary btn-sm">View Details</a>
                    </div>
                </div>
            `;
        });
        appListContainer.innerHTML = appCardsHTML;
    } else {
        appListContainer.innerHTML = '<p>No apps available at the moment.</p>';
    }
});