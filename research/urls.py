from django.urls import path
from . import views

app_name = 'research'

urlpatterns = [
    # path('<slug:slug>/', views.base_project, name='projects'),
    path('', views.base_project, name='projects'),
    path('history/<int:pk>/', views.project_history, name='history'),
    path('history/create/', views.HistoryCreateView.as_view(), name="create"),
    path('purechain/', views.purechain_view, name='purechain_view'),
    path('acknowl/', views.acknowl_view, name='acknowl_view'),
    path('purechain/delete/<path:filename>/', views.delete_file, name='delete_file'),
    path('acknowl/delete/<path:filename>/', views.ackdelete_file, name='ackdelete_file'),
    path('details/<str:title>/', views.entry_details, name='entry_details'),
    path('ackdetails/<str:title>/', views.ackentry_details, name='ackentry_details'),
    path('ackentry/<str:entry_id>/edit/', views.ackentry_edit, name='ackentry_edit'),
]