from django.contrib import admin

from .models import Question, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Set publish date", {"fields": ["pub_date"], "classes": ["collapse"]}),
        ("Set end date", {"fields": ["end_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ["question_text", "pub_date", "was_published_recently", "end_date"]
    list_filter = ["pub_date"]


admin.site.register(Choice)
admin.site.register(Question, QuestionAdmin)
