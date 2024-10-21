from django.contrib import admin
from .models import Posts,AboutusPage,Event

admin.site.register(Posts)



@admin.register(AboutusPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'author')
    search_fields = ('title', 'description')