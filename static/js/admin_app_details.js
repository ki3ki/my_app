
console.log("Static file test: Loaded successfully!");

document.addEventListener('DOMContentLoaded', function() {
    const appId = getAppIdFromUrl(); // Extract app ID from URL (assuming it's passed in the URL)

    if (appId) {
        loadAppDetails(appId);
    }

    document.getElementById('editButton').addEventListener('click', function() {
        toggleEditFields(true);
    });

    document.getElementById('cancelEditButton').addEventListener('click', function() {
        toggleEditFields(false);
    });

    document.getElementById('editForm').addEventListener('submit', function(event) {
        event.preventDefault();
        saveChanges(appId);
    });

    document.getElementById('deleteButton').addEventListener('click', function() {
        deleteApp(appId);
    });
});

// Fetch app details by appId
async function loadAppDetails(appId) {
    const token = localStorage.getItem('access');
    try {
        const response = await fetch(`/adminapp/api/apps/${appId}/`, {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            }
        });

        if (!response.ok) throw new Error('Failed to fetch app details');

        const app = await response.json();
        console.log(app);

        // Populate app details
        document.getElementById('appName').textContent = app.name;
        document.getElementById('appLink').textContent = app.download_link;
        document.getElementById('appLink').href = app.download_link;
        document.getElementById('appCategory').textContent = app.category;
        document.getElementById('appSubcategory').textContent = app.subcategory;
        document.getElementById('appDescription').textContent = app.description;
        document.getElementById('appPoints').textContent = app.points;
        document.getElementById('appLogo').src = app.logo;

        // Pre-fill the edit form with current details
        document.getElementById('editAppName').value = app.name;
        document.getElementById('editAppLink').value = app.download_link;
        document.getElementById('editAppCategory').value = app.category;
        document.getElementById('editAppSubcategory').value = app.subcategory;
        document.getElementById('editAppDescription').value = app.description;
        document.getElementById('editAppPoints').value = app.points;
        document.getElementById('editAppLogo').value = app.logo;

    } catch (error) {
        console.error('Error loading app details:', error);
        showAlert('Error loading app details', 'danger');
    }
}

// Save changes to the app details
async function saveChanges(appId) {
    const token = localStorage.getItem('access');
    const updatedAppData = {
        name: document.getElementById('editAppName').value,
        download_link: document.getElementById('editAppLink').value,
        category: document.getElementById('editAppCategory').value,
        subcategory: document.getElementById('editAppSubcategory').value,
        description: document.getElementById('editAppDescription').value,
        points: parseInt(document.getElementById('editAppPoints').value),
        logo: document.getElementById('editAppLogo').value
    };

    try {
        const response = await fetch(`/adminapp/api/apps/${appId}/`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(updatedAppData),
        });

        if (!response.ok) throw new Error('Failed to save changes');

        showAlert('App details updated successfully!', 'success');
        loadAppDetails(appId); // Reload the updated details

        toggleEditFields(false); // Hide edit form after saving
    } catch (error) {
        console.error('Error saving changes:', error);
        showAlert('Error saving changes', 'danger');
    }
}

// Delete app by appId
async function deleteApp(appId) {
    const token = localStorage.getItem('access');
    try {
        const response = await fetch(`/adminapp/api/apps/${appId}/`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            }
        });

        if (!response.ok) throw new Error('Failed to delete app');

        showAlert('App deleted successfully!', 'success');
        window.location.href = '/adminapp/apps/'; // Redirect to apps list page
    } catch (error) {
        console.error('Error deleting app:', error);
        showAlert('Error deleting app', 'danger');
    }
}

// Show alert message
function showAlert(message, type) {
    let alertDiv = document.getElementById('alertMessage');
    if (!alertDiv) {
        alertDiv = document.createElement('div');
        alertDiv.id = 'alertMessage';
        alertDiv.className = 'alert mt-3';
        document.querySelector('.app-details').insertBefore(alertDiv, document.getElementById('addAppForm'));
    }

    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    alertDiv.style.display = 'block';

    setTimeout(() => {
        alertDiv.style.display = 'none';
    }, 3000);
}

// Toggle edit fields visibility
function toggleEditFields(show) {
    const editFields = document.getElementById('editFields');
    const appInfo = document.querySelector('.app-info');
    const editButton = document.getElementById('editButton');
    
    if (show) {
        editFields.style.display = 'block';
        appInfo.style.display = 'none';
        editButton.style.display = 'none';
    } else {
        editFields.style.display = 'none';
        appInfo.style.display = 'block';
        editButton.style.display = 'inline-block';
    }
}

// Helper function to get appId from URL (for dynamic app pages)
function getAppIdFromUrl() {
    const pathParts = window.location.pathname.split('/'); // Split the URL path into parts
    return pathParts[pathParts.length - 2]; // Assuming the app ID is the second-to-last part of the path
}
