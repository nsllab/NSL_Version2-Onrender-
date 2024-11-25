from django.urls import path
from . import views

app_name = 'research'

urlpatterns = [
    # path('<slug:slug>/', views.base_project, name='projects'),
    path('', views.base_project, name='projects'),
    path('history/<int:pk>/', views.project_history, name='history'),
    path('history/create/', views.HistoryCreateView.as_view(), name="create"),
    path('purechain/', views.purechain_view, name='purechain_view'),
    path('purechain/delete/<int:pk>/', views.delete_entry, name='delete_entry'),
]