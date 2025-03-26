
document.addEventListener('DOMContentLoaded', function() {
    loadCategories();
    setupCategoryForm();
});

async function loadCategories() {
    const token = localStorage.getItem('access');
    try {
        const response = await fetch('/adminapp/api/categories/', {
            headers: {
               'Authorization': `Bearer ${token}`,
               'Content-Type': 'application/json',
            }
        });
        
        if (!response.ok) throw new Error('Failed to fetch categories');
        
        const categories = await response.json();
        displayCategories(categories);
    } catch (error) {
        console.error('Error loading categories:', error);
        showAlert('Error loading categories', 'danger');
    }
}

function displayCategories(categories) {
    const categoryList = document.getElementById('categoryList');
    if (!categoryList) return;

    categoryList.innerHTML = categories.map(category => `
        <div class="card mb-1 p-2" data-category-id="${category.id}" style="height: 60px;">
            <div class="card-body d-flex justify-content-between align-items-center">
                <h5 class="card-title mb-0">${category.name}</h5>
                <div class="btn-group">
                    <button class="btn btn-sm btn-primary edit-category" data-id="${category.id}">Edit</button>
                    <button class="btn btn-sm btn-danger delete-category" data-id="${category.id}">Delete</button>
                </div>
            </div>
        </div>
    `).join('');

    // Add event listeners for edit and delete buttons
    setupCategoryEventListeners();
}

function setupCategoryForm() {
    const form = document.getElementById('categoryForm');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const categoryName = document.getElementById('categoryName').value;
        const categoryId = form.dataset.categoryId;
        
        const token = localStorage.getItem('access');
        try {
            const url = categoryId ? 
                `/adminapp/api/categories/${categoryId}/` : 
                '/adminapp/api/categories/';
            
            const method = categoryId ? 'PUT' : 'POST';
            
            const response = await fetch(url, {
                method: method,
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ name: categoryName })
            });

            if (!response.ok) throw new Error('Failed to save category');

            showAlert(`Category ${categoryId ? 'updated' : 'created'} successfully`, 'success');
            form.reset();
            form.removeAttribute('data-category-id');
            loadCategories();
        } catch (error) {
            console.error('Error saving category:', error);
            showAlert('Error saving category', 'danger');
        }
    });
}

function setupCategoryEventListeners() {
    // Edit category
    document.querySelectorAll('.edit-category').forEach(button => {
        button.addEventListener('click', async (e) => {
            const categoryId = e.target.dataset.id;
            const categoryCard = document.querySelector(`[data-category-id="${categoryId}"]`);
            const categoryName = categoryCard.querySelector('.card-title').textContent;
            
            const form = document.getElementById('categoryForm');
            form.dataset.categoryId = categoryId;
            document.getElementById('categoryName').value = categoryName;
        });
    });

    // Delete category
    document.querySelectorAll('.delete-category').forEach(button => {
        button.addEventListener('click', async (e) => {
            if (!confirm('Are you sure you want to delete this category?')) return;
            
            const categoryId = e.target.dataset.id;
            const token = localStorage.getItem('access');
            
            try {
                const response = await fetch(`/adminapp/api/categories/${categoryId}/`, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                    }
                });

                if (!response.ok) throw new Error('Failed to delete category');

                showAlert('Category deleted successfully', 'success');
                loadCategories();
            } catch (error) {
                console.error('Error deleting category:', error);
                showAlert('Error deleting category', 'danger');
            }
        });
    });
}

function showAlert(message, type) {
    const alertDiv = document.getElementById('alertMessage');
    if (alertDiv) {
        alertDiv.className = `alert alert-${type}`;
        alertDiv.textContent = message;
        alertDiv.style.display = 'block';
        setTimeout(() => alertDiv.style.display = 'none', 3000);
    }
}