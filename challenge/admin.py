from django.contrib import admin

# Register your models here.

from .models import Challenge

@admin.register(Challenge)
class NoteAdmin(admin.ModelAdmin):
    list_filter = ('day_created',)
    list_display = ('name', 'day_created', 'date_start', 'date_end', 'description')
#admin.site.register(Challenge)