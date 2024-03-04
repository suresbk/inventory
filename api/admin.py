'''Django admin customization'''

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UA
from . import models


class UserAdmin(UA):
    '''Admin page customizations'''
    ordering = ['id']
    list_display = ['mobile', 'name']
    search_fields = ['mobile']
    list_filter = ('mobile',)
    fieldsets = (
        (None, {'fields': ('mobile', 'password')}),
        (
            ('Permissions'),
            {
                'fields': ('is_active', 'is_staff', 'is_executive', 'is_superuser',)
            }
        ),
        (('Timings'), {'fields': ('last_login',)},)
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'mobile',
                'password',
                'name',
                'is_active',
                'is_staff',
                'is_executive',
                'is_superuser',
            )
        }

        ),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Manufacturer)
admin.site.register(models.Brand)
# admin.site.register(models.Category)
admin.site.register(models.Variant)
admin.site.register(models.Product)

