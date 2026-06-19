from django.contrib import admin
from .models import Internship, PlacementDrive
from .models import Application
from .models import InternshipOpportunity, InternshipApplication


admin.site.register(Internship)
admin.site.register(PlacementDrive)
admin.site.register(Application)
admin.site.register(InternshipOpportunity)
admin.site.register(InternshipApplication)
