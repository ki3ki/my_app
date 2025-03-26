document.addEventListener('DOMContentLoaded', function() {
    loadCategories();
    setupImagePreview();
    setupFormSubmission();
    setupAddAppButton();
});

// Handle image upload and preview
function setupImagePreview() {
    const imageInput = document.getElementById('appImage');
    const imagePlaceholder = document.querySelector('.image-placeholder');

    imageInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(event) {
                // Create image preview
                imagePlaceholder.innerHTML = `
                    <img src="${event.target.result}" 
                         alt="App Logo Preview" 
                         style="max-width: 100%; max-height: 200px; object-fit: contain;">
                `;
            };
            reader.readAsDataURL(file);
        } else {
            // Reset to default placeholder
            imagePlaceholder.innerHTML = '<i class="bi bi-image"></i>';
        }
    });
}

// Load categories into dropdown
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
    const categorySelect = document.getElementById('appCategory');
    if (!categorySelect) return;

    categorySelect.innerHTML = '<option value="">Select Category</option>' +
        categories.map(category => 
            `<option value="${category.id}">${category.name}</option>`
        ).join(''); 

    // Add event listener for category change
    categorySelect.addEventListener('change', function() {
        loadSubcategories(this.value);
    });
}

// Load subcategories based on selected category
async function loadSubcategories(categoryId) {
    if (!categoryId) {
        resetSubcategoryDropdown();
        return;
    }

    const token = localStorage.getItem('access');
    try {
        const response = await fetch(`/adminapp/api/subcategories/?category=${categoryId}`, {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            }
        });
        
        if (!response.ok) throw new Error('Failed to fetch subcategories');
        
        const subcategories = await response.json();
        populateSubcategoryDropdown(subcategories.data || subcategories);
    } catch (error) {
        console.error('Error loading subcategories:', error);
        showAlert('Error loading subcategories', 'danger');
    }
}

function resetSubcategoryDropdown() {
    const subcategorySelect = document.getElementById('appSubCategory');
    if (subcategorySelect) {
        subcategorySelect.innerHTML = '<option value="">Select Category First</option>';
        subcategorySelect.disabled = true;
    }
}

function populateSubcategoryDropdown(subcategories) {
    const subcategorySelect = document.getElementById('appSubCategory');
    if (!subcategorySelect) return;

    subcategorySelect.innerHTML = '<option value="">Select Subcategory</option>' +
        subcategories.map(subcategory => 
            `<option value="${subcategory.id}">${subcategory.name}</option>`
        ).join('');
    subcategorySelect.disabled = false;
}

// Set up the "Add App" button behavior
function setupAddAppButton() {
    const addAppButton = document.getElementById('addAppButton');
    const addPointsButton = document.getElementById('addPointsButton');
    const pointsRow = document.getElementById('points-row');

    // Initially, the points input should be hidden
    pointsRow.style.display = 'none';
    addPointsButton.classList.add('d-none');

    addAppButton.addEventListener('click', function(e) {
        e.preventDefault();
        
        // Show points input and change the button to Add Points
        pointsRow.style.display = 'block';
        addAppButton.classList.add('d-none');
        addPointsButton.classList.remove('d-none');
    });
    
    addPointsButton.addEventListener('click', function(e) {
        e.preventDefault();
        
        const appName = document.getElementById('appName').value;
        const appLink = document.getElementById('appLink').value;
        const categoryId = document.getElementById('appCategory').value;
        const subcategoryId = document.getElementById('appSubCategory').value;
        const points = document.getElementById('points').value;
        const imageFile = document.getElementById('appImage').files[0];

        // Validate points input
        if (!points || points <= 0) {
            showAlert('Please enter a valid point value.', 'warning');
            return;
        }

        // Create FormData to send to the server
        const formData = new FormData();
        formData.append('name', appName);
        formData.append('download_link', appLink);
        formData.append('category', categoryId);
        formData.append('subcategory', subcategoryId);
        formData.append('points', points); // Add points to form data
        if (imageFile) {
            formData.append('logo', imageFile);
        }

        // Send app data to the server
        const token = localStorage.getItem('access');
        fetch('/adminapp/api/apps/', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showAlert('App created successfully!', 'success');
                resetForm();
            } else {
                showAlert('Error creating app', 'danger');
            }
        })
        .catch(error => {
            console.error('Error creating app:', error);
            showAlert('Error creating app', 'danger');
        });
    });
}

// Handle form submission
function setupFormSubmission() {
    const form = document.getElementById('addAppForm');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
    });
}

// Reset the form and buttons
function resetForm() {
    const form = document.getElementById('addAppForm');
    form.reset();
    resetImagePreview();
    resetSubcategoryDropdown();

    // Reset points input and buttons
    document.getElementById('points-row').style.display = 'none';
    document.getElementById('addAppButton').classList.remove('d-none');
    document.getElementById('addPointsButton').classList.add('d-none');
}

// Reset image preview
function resetImagePreview() {
    const imagePlaceholder = document.querySelector('.image-placeholder');
    if (imagePlaceholder) {
        imagePlaceholder.innerHTML = '<i class="bi bi-image"></i>';
    }
}

function showAlert(message, type) {
    // Create alert element if it doesn't exist
    let alertDiv = document.getElementById('alertMessage');
    if (!alertDiv) {
        alertDiv = document.createElement('div');
        alertDiv.id = 'alertMessage';
        alertDiv.className = 'alert mt-3';
        document.querySelector('.app-form').insertBefore(alertDiv, document.getElementById('addAppForm'));
    }

    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    alertDiv.style.display = 'block';

    // Hide after 3 seconds
    setTimeout(() => {
        alertDiv.style.display = 'none';
    }, 3000);
}
