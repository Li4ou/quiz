from progress.models import Progress,Achievements

from django.contrib import admin




@admin.register(Achievements)
class AchievementsAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'id']

admin.site.register(Progress)
# Register your models here.
