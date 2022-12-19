from django.contrib import admin

# Register your models here.

from .models import Challenge, Quizz, Hint, Answer

class siteAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)  
admin.site.register(Challenge,siteAdmin)
admin.site.register(Hint,siteAdmin)
admin.site.register(Quizz,siteAdmin)
admin.site.register(Answer,siteAdmin)
# class NoteAdmin(admin.ModelAdmin):
#     list_filter = ('day_created',)
#     list_display = ('name', 'day_created', 'date_start', 'date_end', 'description')
# admin.site.register(Challenge)