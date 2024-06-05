from django.contrib import admin
from .models import Customer

class LabelAdmin(admin.ModelAdmin):

    list_display = ('id', 'fullname', 'phone', 'created_at')

    def fullname (self, obj):
        return f"{obj.firstname} {obj.lastname}"
    
    fullname.short_description = 'Full Name'

admin.site.register(Customer, LabelAdmin)
