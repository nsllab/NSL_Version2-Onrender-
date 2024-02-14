from django.contrib import admin
from .models import Journal, Conference, Patent, Book
# Register your models here.

class JournalAdmin(admin.ModelAdmin):
    search_fields = ['journal_type']
    list_display = ('id', 'title', 'journal_type',)

class ConferenceAdmin(admin.ModelAdmin):
    search_fields = ['conference_type']
    list_display = ('id', 'title', 'conference_type',)

# class PatentAdmin(admin.ModelAdmin):
#     list_filter = ('patent_type',)

admin.site.register(Conference, ConferenceAdmin)
admin.site.register(Journal, JournalAdmin)
admin.site.register(Patent)
admin.site.register(Book)