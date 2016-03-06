from django.contrib import admin

from .models import Question, Choice

class ChoiceInline(admin.StackedInline):
	extra = 3
	model = Choice

class QuestionAdmin(admin.ModelAdmin):
	fieldsets = [(None, {'fields': ['question_text']}), ('Date Information', {'fields': ['pub_date']})]
	inlines = [ChoiceInline]

	list_display = ('question_text', 'pub_date', 'was_published_in_last_7_days')

	list_filter = ['pub_date']
	search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)