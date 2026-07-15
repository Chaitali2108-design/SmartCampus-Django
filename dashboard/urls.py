from django.urls import path
from . import views
from django.urls import include

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

    #for job preparation page
    path("preparation/", views.preparation, name="preparation"),
    path("preparation/<str:test_type>/<str:page>/",views.preparation_test,name="preparation_test",),
    path("preparation/result/",views.preparation_result,name="preparation_result"),
    path(
    "preparation/generate-questions/",
    views.generate_questions,
    name="generate_questions",
),

   #coding api connect url
   path(
    "api/",
    include("dashboard.api.urls")
),
 #for communication page
 path(
    "preparation/communication/",
    views.communication_test,
    name="communication_test"
),

path(
    "preparation/coding/result/",
    views.coding_result,
    name="coding_result",
),
]  
    