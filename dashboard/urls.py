from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing, name="landing"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("placements/", views.placements, name="placements"),
    path("profile/", views.profile, name="profile"),
    path("accounts/signup/", views.signup, name="signup"),
    path("apply/<int:pk>/", views.apply_job, name="apply_job"),
    path("my-applications/", views.my_applications, name="my_applications"),
    path("roadmap/", views.ai_roadmap, name="ai_roadmap"),
    path("internships/", views.internships, name="internships"),
    path("internships/<int:pk>/apply/", views.apply_internship, name="apply_internship"),
    path("recruiter/",views.recruiter_dashboard,name="recruiter_dashboard"),
    path("preparation/", views.preparation, name="preparation"),
    path("preparation/test/<int:round_id>/",views.preparation_test,name="preparation_test"),
]  
