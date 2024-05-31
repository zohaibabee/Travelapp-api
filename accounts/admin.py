from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from django.contrib import admin

class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ['email', 'name', 'is_admin', 'is_active']
    search_fields = ['email', 'name']
    ordering = ['email']


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
