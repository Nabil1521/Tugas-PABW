from django.contrib import admin
from .models import Car


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['id', 'carname', 'carbrand', 'carmodel', 'carprice']
    search_fields = ['carname', 'carbrand', 'carmodel']
