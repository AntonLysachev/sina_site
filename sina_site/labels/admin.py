from django.contrib import admin
from .models import Label


class LabelAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'created_at')


admin.site.register(Label, LabelAdmin)
