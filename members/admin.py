from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Member, Bio

class MemberAdmin(UserAdmin):
    # Define your custom configurations for the Member model admin here
    list_display = ('username', 'password', 'email', 'login_cnt', 'last_login', 'is_active', 'is_staff', 'is_superuser', 'first_name')
    # fieldsets = (
    #     # Include your custom fields in the fieldsets as needed
    #     (None, {'fields': ('username', 'password')}),
    #     ('Personal info', {'fields': ('email', 'login_cnt')}),
    #     ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    #     ('Important dates', {'fields': ('last_login', 'date_joined')}),
    # )

# Unregister the default User model
# admin.site.unregister(Member)
class BioAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_order', 'position',)
    search_fields = ['name', 'position']
    list_filter = ('position',)
    

admin.site.register(Member, MemberAdmin)
admin.site.register(Bio, BioAdmin)
