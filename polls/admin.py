from django.contrib import admin

# Register your models here.
from .models import Question # import Question 
from .models import Choice
class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 0 # numbers extra which choice if want to add in
class QuestionAdmin(admin.ModelAdmin):
    fileds = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes':['collapse']}),
    ]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    inlines = [ChoiceInLine]
admin.site.register(Question, QuestionAdmin)