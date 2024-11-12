from django.urls import path

from . import views

app_name = 'publications'

urlpatterns = [
    path('journals', views.journals, name='journals'),
    path('stats/journals', views.all_journals, name='all_journals'),
    path('journals/create', views.JournalCreateView.as_view(), name='journal_create'),
    path('journals/update/<int:pk>', views.JournalUpdateView.as_view(), name='journal_update'),
    path('journals/<int:pk>', views.JournalDetailView.as_view(), name='journal_detail'),

    
    path('conferences', views.conferences, name='conferences'),
    path('conferences/domestic/', views.domestic_conferences, name='domestic_conferences'),
    path('conferences/international/', views.international_conferences, name='international_conferences'),
    path('stats/conferences', views.all_conferences, name='all_conferences'),
    path('conferences/create', views.ConferenceCreateView.as_view(), name='conference_create'),
    path('conferences/update/<int:pk>', views.ConferenceUpdateView.as_view(), name='conference_update'),
    path('conferences/<int:pk>', views.ConferenceDetailView.as_view(), name='conference_detail'),

    path('patents', views.patents, name="patents"),
    path('patents/<int:pk>/update', views.PatentUpdateView.as_view(), name="patent_update"),
    path('patents/create', views.PatentCreateView.as_view(), name="patent_create"),

    path('books', views.books, name="books"),
    path('books/create', views.BookCreateView.as_view(), name="book_create"),
    path('books/<int:pk>/update', views.BookUpdateView.as_view(), name="book_update"),
]