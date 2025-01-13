from django.urls import path
from . import views

app_name = 'members'

urlpatterns = [
    # other paths...
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('logout/', views.logout_user, name='logout'),

    path('profile/update/', views.MemberUpdateView.as_view(), name='update_profile'),
    path('<int:pk>/password/',views. MemberChangePasswordView.as_view(), name='change_password'),

    path('profile/<int:pk>/update/',views. BioUpdateView.as_view(), name='bio_update'),

    path('professors/', views.ProfessorsListView.as_view(), name="professors_list"),

    path('post_docs/', views.PostDocsListView.as_view(), name="post_docs_list"),
    path('post_docs/<int:pk>', views.PostDocDetailView.as_view(), name="post_docs_detail"),

    path('full_time/', views.FullTimeListView.as_view(), name="full_time_list"),
    path('full_time/<int:pk>', views.FullTimeDetailView.as_view(), name="full_time_detail"),

    path('part_time/', views.PartTimeListView.as_view(), name="part_time_list"),
    # path('full_time/<int:pk>', views.FullTimeDetailView.as_view(), name="full_time_detail"),

    path('visiting/', views.VisitingListView.as_view(), name="visiting_list"),

    path('alumni_post_doc/', views.AlumniPostDocListView.as_view(), name="alumni_post_doc"),

    path('alumni_graduate/', views.AlumniGraduateListView.as_view(), name="alumni_graduate"),

    path('advisers/', views.AdvisersListView.as_view(), name="advisers"),

    path('undergraduate/', views.UnderGraduateListView.as_view(), name="undergraduate"),

    # path('alumni_post_doc/', views.AlumniPostDocListView.as_view(), name="alumni_post_doc"),

]
