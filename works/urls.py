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
    path('seminars/create', views.SeminarCreateView.as_view(), name='create_seminar'),
    path('seminars/<int:pk>/update', views.SeminarUpdateView.as_view(), name="seminar_update"),

    path('reviews/', views.ReviewListView.as_view(), name='reviews'),
    path('reviews/create', views.ReviewCreateView.as_view(), name='create_review'),
    path('reviews/<int:pk>/update', views.ReviewUpdateView.as_view(), name="review_update"),

    path('pt', views.PaperTemplateListView.as_view(), name='paper_templates'),
    path('pt/create', views.PaperTemplateCreateView.as_view(), name='create_paper_template'),
    path('pt/<int:pk>/update', views.PaperTemplateUpdateView.as_view(), name="paper_template_update"),
    path('pt/<int:pk>/', views.PaperTemplateDetailView.as_view(), name='paper_template_detail'),

    path('weekly-reports/', views.weekly_reports_migration, name='weekly_reports'),

]