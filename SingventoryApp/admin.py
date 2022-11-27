from django.contrib import admin
from SingventoryApp.models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

class UserAdminConfig(UserAdmin):
    model = SVUser
    search_fields = ('email', 'name')
    list_filter = ( 'email', 'name', 'is_staff')
    ordering = ('email',)
    list_display = ('name', 'email','category', 'is_staff')

    fieldsets = (
        (None, {'fields': ( 'email', 'name','category','image','password','activated')}),
        ('Permissions', {'fields': ('is_active','is_staff','user_permissions')}),
    )

    add_fieldsets = (
        (
            None, {
                'classes': ('wide',),
                'fields': ( 'email', 'name','password1', 'password2','category','image','is_active', 'is_staff','activated','user_permissions'),
            }
        ),
    )

    
class BorrowAdmin(admin.ModelAdmin):
    list_display = ('user', 'equipment','quantity', 'date','status')

class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name','quantity', 'category','visibility')

# Register your models here.
admin.site.register(SVUser, UserAdminConfig)
admin.site.register(Category)
admin.site.register(Equipment,EquipmentAdmin)
admin.site.register(Borrow, BorrowAdmin)
admin.site.register(Notification)