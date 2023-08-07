from django.contrib import admin
from .models import CustomUser

# admin.site.register(CustomUser)
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'phone_no', 'is_active', 'is_staff', 'is_superuser']
    list_filter = ['is_active', 'is_staff', 'is_superuser']
    search_fields = ['username', 'email', 'phone_no']
    ordering = ['username']