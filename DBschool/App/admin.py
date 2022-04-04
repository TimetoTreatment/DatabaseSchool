from django.contrib import admin

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = (
        'user_id',
        'user_pw',
        'user_name',
        'user_identity',
        'user_register_time',
    )