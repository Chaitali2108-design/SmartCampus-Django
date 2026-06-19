from django.db import models
from django.contrib.auth.models import User


class Internship(models.Model):
    company = models.CharField(max_length=100)
    initial = models.CharField(max_length=5)
    role = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    stipend = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    is_trending = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.company} - {self.role}"


class PlacementDrive(models.Model):
    company = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    package = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    mode = models.CharField(max_length=50)
    deadline = models.DateField()

    def __str__(self):
        return self.company
    
class KPI(models.Model):
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=50)
    icon = models.CharField(max_length=50)

    def __str__(self):
        return self.label
    
class Metric(models.Model):
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=50)
    text = models.CharField(max_length=100)
    width = models.CharField(max_length=20)
    gradient = models.CharField(max_length=100)

    def __str__(self):
        return self.label
    
class Activity(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    


class StudentProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    full_name = models.CharField(max_length=100)

    college = models.CharField(
        max_length=200,
        blank=True,
        default=""
    )

    branch = models.CharField(
        max_length=100,
        blank=True,
        default=""
    )

    year = models.CharField(
        max_length=20,
        blank=True,
        default=""
    )

    skills = models.TextField(
        blank=True,
        default=""
    )

    bio = models.TextField(
        blank=True,
        default=""
    )

    github = models.URLField(
        blank=True,
        default=""
    )

    linkedin = models.URLField(
        blank=True,
        default=""
    )

    phone = models.CharField(
        max_length=15,
        blank=True,
        default=""
    )

    location = models.CharField(
        max_length=100,
        blank=True,
        default=""
    )

    profile_photo = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True
    )

    resume = models.FileField(
        upload_to="resumes/",
        blank=True,
        null=True
    )

    email = models.EmailField(
        blank=True,
        default=""
    )

    cgpa = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.full_name
    
class Application(models.Model):

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE
    )

    placement = models.ForeignKey(
        PlacementDrive,
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=30,
        default="Applied"
    )

    applied_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.student.full_name} - {self.placement.company}"
    

class AIRoadmap(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    current_skills = models.TextField()

    target_role = models.CharField(
        max_length=100
    )

    roadmap = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.target_role
    

class InternshipOpportunity(models.Model):
    role = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    stipend = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    skills = models.TextField()
    trending = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role} - {self.company}"
    

class InternshipApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    internship = models.ForeignKey(
        InternshipOpportunity,
        on_delete=models.CASCADE,
        related_name="applications"
    )
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'internship')