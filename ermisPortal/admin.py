from django.contrib import admin

# Register your models here.
#from django.conf import settings
#from .models import User

# Register your models here.
#admin.site.register(User)
from django.contrib.auth import admin as auth_admin
from .models import User

class ErmisAdmin(auth_admin.UserAdmin):
    pass
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'department')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',#)}),
                                       'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('gn_is_active', 'gn_is_staff')}
        ),
    )
    readonly_fields = ('last_login', 'date_joined',)

admin.site.register(User, ErmisAdmin)
