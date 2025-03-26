

from django.contrib import admin
from .models import AppCategory, AppSubCategory, App




admin.site.register(AppCategory)
admin.site.register(AppSubCategory)
admin.site.register(App)

