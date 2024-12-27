from django.contrib import admin

# Register your models here.
from .models import Dashboard

class DashboardAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_posted', 'author')

admin.site.register(Dashboard, DashboardAdmin)