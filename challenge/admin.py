from django.contrib import admin

# Register your models here.

from .models import Challenge, Quizz, Hint

admin.site.register(Challenge)
admin.site.register(Hint)
class QuizzAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)   
admin.site.register(Quizz,QuizzAdmin)
# class NoteAdmin(admin.ModelAdmin):
#     list_filter = ('day_created',)
#     list_display = ('name', 'day_created', 'date_start', 'date_end', 'description')
# admin.site.register(Challenge)