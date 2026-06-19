from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from dashboard.forms import LoginForm

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('dashboard.urls')),

    path(
        "accounts/login/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html",
            authentication_form=LoginForm
        ),
        name="login",
    ),

    path("accounts/", include("django.contrib.auth.urls")),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)