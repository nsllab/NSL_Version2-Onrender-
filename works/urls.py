from django.urls import path
from . import views

app_name = "works"

urlpatterns = [
    path('weekly_reports', views.weekly_reports, name='weekly_reports'),
    path('create', views.WeeklyReportCreateView.as_view(), name='create_report'),
    path('<int:pk>/details', views.WeeklyReportDetailView.as_view(), name='details'),
    path('<int:pk>/update', views.WeeklyReportUpdateView.as_view(), name='update'),


    path('post_docs/', views.post_doc_reports, name='post_doc_reports'),
    path('post_doc/create', views.PostDocReportCreateView.as_view(), name="post_doc_create"),
    path('post_doc/<int:pk>/details', views.PostDocReportDetailView.as_view(), name="post_doc_details"),
    path('post_doc/<int:pk>/update', views.PostReportUpdateView.as_view(), name="post_doc_update"),

    path('seminars/', views.seminars, name='seminars'),
    path('create', views.SeminarCreateView.as_view(), name='create_seminar'),
    path('seminars/<int:pk>/update', views.PostReportUpdateView.as_view(), name="seminar_update"),
]