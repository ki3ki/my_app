from django.db import models

class AppCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class AppSubCategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        AppCategory, 
        on_delete=models.CASCADE,  # Deleting a category will delete its subcategories
        related_name="subcategories"  # Allows accessing subcategories of a category using 'category.subcategories'
    )

    def __str__(self):
        return self.name 


class App(models.Model):
    name = models.CharField(max_length=255) 
    description = models.TextField(null=True) 
    points = models.PositiveIntegerField(null=True)  
    created_at = models.DateTimeField(auto_now_add=True, null=True)  
    updated_at = models.DateTimeField(auto_now=True, null=True)  
    category = models.ForeignKey(
        AppCategory, 
        on_delete=models.SET_NULL,  # If the category is deleted, set the category to NULL
        null=True, 
        blank=True
    )
    subcategory = models.ForeignKey(
        AppSubCategory, 
        on_delete=models.SET_NULL,  # If the subcategory is deleted, set the subcategory to NULL
        null=True, 
        blank=True
    )
    logo = models.ImageField(
        upload_to="app_logos/", 
        null=True, 
        blank=True  # Allow apps without a logo
    )
    download_link = models.URLField(
        max_length=200, 
        null=True, 
        blank=True, 
    
    )

    def __str__(self):
        return self.name


