from django.contrib import admin
from .models import Status


class StatusAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'created_at')


admin.site.register(Status, StatusAdmin)
