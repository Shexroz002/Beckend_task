from django.contrib import admin
from .models import CustomUser


# Register your models here.


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role')
    search_fields = ('username', 'email', 'role')
    list_filter = ('role',)

    ordering = ('username',)
    filter_horizontal = ()
    readonly_fields = ('date_joined', 'last_login')
    list_per_page = 10


admin.site.register(CustomUser, CustomUserAdmin)
