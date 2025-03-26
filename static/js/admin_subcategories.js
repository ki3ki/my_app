document.addEventListener('DOMContentLoaded', function() {
    loadCategories();
    loadSubcategories();
    setupSubcategoryForm();
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
        populateCategoryDropdown(categories);
    } catch (error) {
        console.error('Error loading categories:', error);
        showAlert('Error loading categories', 'danger');
    }
}

function populateCategoryDropdown(categories) {
    const select = document.getElementById('categorySelect');
    if (!select) return;

    select.innerHTML = '<option value="">Choose a category...</option>' +
        categories.map(category => 
            `<option value="${category.id}">${category.name}</option>`
        ).join('');
}

async function loadSubcategories() {
    const token = localStorage.getItem('access');
    try {
        const response = await fetch('/adminapp/api/subcategories/', {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            }
        });
        
        if (!response.ok) throw new Error('Failed to fetch subcategories');
        
        const subcategories = await response.json();
        displaySubcategories(subcategories);
    } catch (error) {
        console.error('Error loading subcategories:', error);
        showAlert('Error loading subcategories', 'danger');
    }
}

async function displaySubcategories(subcategories) {
    const subcategoryList = document.getElementById('subcategoryList');
    if (!subcategoryList) return;

    // Fetch categories to get category names
    const token = localStorage.getItem('access');
    const categoriesResponse = await fetch('/adminapp/api/categories/', {
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
        }
    });
    const categories = await categoriesResponse.json();
    const categoryMap = Object.fromEntries(categories.map(cat => [cat.id, cat.name]));

    subcategoryList.innerHTML = subcategories.map(subcategory => `
        <div class="card mb-3" data-subcategory-id="${subcategory.id}" style="height: 60px;">
            <div class="card-body d-flex justify-content-between align-items-center">
                <div>
                    <h5 class="card-title mb-0">${subcategory.name}</h5>
                    <small class="text-muted">Category: ${categoryMap[subcategory.category] || 'Unknown'}</small>
                </div>
                <div class="btn-group">
                    <button class="btn btn-sm btn-primary edit-subcategory" 
                            data-id="${subcategory.id}" 
                            data-name="${subcategory.name}"
                            data-category="${subcategory.category}">Edit</button>
                    <button class="btn btn-sm btn-danger delete-subcategory" 
                            data-id="${subcategory.id}">Delete</button>
                </div>
            </div>
        </div>
    `).join('');

    setupSubcategoryEventListeners();
}

function setupSubcategoryForm() {
    const form = document.getElementById('subcategoryForm');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const subcategoryName = document.getElementById('subcategoryName').value;
        const categoryId = document.getElementById('categorySelect').value;
        const subcategoryId = form.dataset.subcategoryId;
        
        if (!categoryId) {
            showAlert('Please select a category', 'warning');
            return;
        }

        const token = localStorage.getItem('access');
        try {
            const url = subcategoryId ? 
                `/adminapp/api/subcategories/${subcategoryId}/` : 
                '/adminapp/api/subcategories/';
            
            const method = subcategoryId ? 'PUT' : 'POST';
            
            const response = await fetch(url, {
                method: method,
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    name: subcategoryName,
                    category: categoryId
                })
            });

            if (!response.ok) throw new Error('Failed to save subcategory');

            showAlert(`Subcategory ${subcategoryId ? 'updated' : 'created'} successfully`, 'success');
            form.reset();
            form.removeAttribute('data-subcategory-id');
            loadSubcategories();
        } catch (error) {
            console.error('Error saving subcategory:', error);
            showAlert('Error saving subcategory', 'danger');
        }
    });
}

function setupSubcategoryEventListeners() {
    // Edit subcategory
    document.querySelectorAll('.edit-subcategory').forEach(button => {
        button.addEventListener('click', (e) => {
            const { id, name, category } = e.target.dataset;
            
            const form = document.getElementById('subcategoryForm');
            form.dataset.subcategoryId = id;
            document.getElementById('subcategoryName').value = name;
            document.getElementById('categorySelect').value = category;
        });
    });

    // Delete subcategory
    document.querySelectorAll('.delete-subcategory').forEach(button => {
        button.addEventListener('click', async (e) => {
            if (!confirm('Are you sure you want to delete this subcategory?')) return;
            
            const subcategoryId = e.target.dataset.id;
            const token = localStorage.getItem('access');
            
            try {
                const response = await fetch(`/adminapp/api/subcategories/${subcategoryId}/`, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                    }
                });

                if (!response.ok) throw new Error('Failed to delete subcategory');

                showAlert('Subcategory deleted successfully', 'success');
                loadSubcategories();
            } catch (error) {
                console.error('Error deleting subcategory:', error);
                showAlert('Error deleting subcategory', 'danger');
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