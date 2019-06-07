from django.contrib import admin

from .models import Question

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Data i godzina publikacji', {'fields': ['pub_date']}),
    ]

admin.site.register(Question, QuestionAdmin)
