from django.contrib import admin
from .models import Review

class LabelAdmin(admin.ModelAdmin):

    list_display = ('id', 'review', 'grade', 'customer_name', 'customer_phone', 'created_at')

    def customer_name(self, obj: Review):
        return f'{obj.customer.firstname} {obj.customer.lastname}'
    
    def customer_phone(self, obj: Review):
        return f'{obj.customer.phone}'
    
    customer_phone.short_description = 'Customer Phone'
    customer_name.short_description = 'Customer Name'

admin.site.register(Review, LabelAdmin)
