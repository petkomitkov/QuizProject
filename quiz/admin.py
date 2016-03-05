from django.contrib import admin
from .models import Question, Choice, Category, Score

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Points Information', {'fields': ['question_points'], 'classes': ['collapse']}),
        ('Category', {'fields': ['category']})
    ]
    inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Category)
admin.site.register(Score)
