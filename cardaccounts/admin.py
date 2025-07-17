from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Social Info', {'fields': ('social_type', 'social_id', 'profile_image')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
