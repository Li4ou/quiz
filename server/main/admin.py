from .models import Quiz, Questions,Results, Answers


from django.contrib import admin
from django.contrib.sessions.models import Session

# Register your models here.


@admin.register(Answers)
class AnswersAdmin(admin.ModelAdmin):
    list_display = ['text', 'correct']

admin.site.register(Quiz)
admin.site.register(Questions)
admin.site.register(Session)
admin.site.register(Results)

