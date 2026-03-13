from django.contrib import admin
from .models import Choice, Question

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    # Organizes the edit page into sections
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    # Adds Choice fields directly to the Question edit page
    inlines = [ChoiceInline]
    
    # Adds the columns to the Questions list page
    list_display = ["question_text", "pub_date", "was_published_recently"]
    
    # Adds the filter sidebar on the right side
    list_filter = ["pub_date"]
    
    # Adds the search box at the top of the list
    # Use questiontext if you renamed the field, otherwise use question_text
    search_fields = ["question_text"]

# Register the Question model with the custom QuestionAdmin settings
admin.site.register(Question, QuestionAdmin)