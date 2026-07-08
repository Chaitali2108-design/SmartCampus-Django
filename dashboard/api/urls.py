from django.urls import path
from .views import run_code_api, submit_code_api


urlpatterns = [
    path("run-code/", run_code_api),
    path("submit-code/", submit_code_api),
]