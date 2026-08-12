from django.db import models
from django.conf import settings


class Resume(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="resumes"
    )

    title = models.CharField(
        max_length=150,
        default="My Resume"
    )

    template = models.CharField(
        max_length=50,
        default="professional"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.title}"


class PersonalInformation(models.Model):

    resume = models.OneToOneField(
        Resume,
        on_delete=models.CASCADE,
        related_name="personal_information"
    )

    full_name = models.CharField(
        max_length=150
    )

    professional_title = models.CharField(
        max_length=150,
        blank=True
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    location = models.CharField(
        max_length=150,
        blank=True
    )

    linkedin = models.URLField(
        blank=True
    )

    github = models.URLField(
        blank=True
    )

    portfolio = models.URLField(
        blank=True
    )

    profile_photo = models.ImageField(
        upload_to="resume/profile/",
        blank=True,
        null=True
    )

    summary = models.TextField(
        blank=True
    )

    def __str__(self):
        return f"Personal Information - {self.full_name}"


class Education(models.Model):

    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name="education"
    )

    institution = models.CharField(
        max_length=200
    )

    degree = models.CharField(
        max_length=150
    )

    field_of_study = models.CharField(
        max_length=150,
        blank=True
    )

    start_date = models.DateField(
        null=True,
        blank=True
    )

    end_date = models.DateField(
        null=True,
        blank=True
    )

    currently_studying = models.BooleanField(
        default=False
    )

    grade = models.CharField(
        max_length=50,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.degree} - {self.institution}"



class Experience(models.Model):

    EXPERIENCE_TYPES = [
        ("full_time", "Full-time"),
        ("part_time", "Part-time"),
        ("internship", "Internship"),
        ("freelance", "Freelance"),
        ("contract", "Contract"),
        ("other", "Other"),
    ]

    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name="experiences"
    )

    experience_type = models.CharField(
        max_length=30,
        choices=EXPERIENCE_TYPES,
        default="full_time"
    )

    company = models.CharField(
        max_length=200
    )

    job_title = models.CharField(
        max_length=150
    )

    location = models.CharField(
        max_length=150,
        blank=True
    )

    start_date = models.DateField(
        null=True,
        blank=True
    )

    end_date = models.DateField(
        null=True,
        blank=True
    )

    currently_working = models.BooleanField(
        default=False
    )

    description = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.job_title} - {self.company}"




class Skill(models.Model):

    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name="skills"
    )

    name = models.CharField(
        max_length=100
    )

    level = models.CharField(
        max_length=50,
        blank=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name



class Project(models.Model):

    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name="resume_projects"
    )

    name = models.CharField(
        max_length=200
    )

    role = models.CharField(
        max_length=150,
        blank=True
    )

    description = models.TextField()

    technologies = models.CharField(
        max_length=500,
        blank=True
    )

    project_url = models.URLField(
        blank=True
    )

    github_url = models.URLField(
        blank=True
    )

    start_date = models.DateField(
        null=True,
        blank=True
    )

    end_date = models.DateField(
        null=True,
        blank=True
    )

    is_current = models.BooleanField(
        default=False
    )

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return self.name




class Certification(models.Model):

    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name="certifications"
    )

    name = models.CharField(
        max_length=200
    )

    issuing_organization = models.CharField(
        max_length=200,
        blank=True
    )

    issue_date = models.DateField(
        null=True,
        blank=True
    )

    credential_id = models.CharField(
        max_length=150,
        blank=True
    )

    credential_url = models.URLField(
        blank=True
    )

    class Meta:
        ordering = ["-issue_date"]

    def __str__(self):
        return self.name


class Achievement(models.Model):

    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name="achievements"
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    date = models.DateField(
        null=True,
        blank=True
    )

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return self.title


class Language(models.Model):

    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name="languages"
    )

    name = models.CharField(
        max_length=100
    )

    proficiency = models.CharField(
        max_length=50,
        blank=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Training(models.Model):

    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name="trainings"
    )

    name = models.CharField(
        max_length=200
    )

    organization = models.CharField(
        max_length=200,
        blank=True
    )

    start_date = models.DateField(
        null=True,
        blank=True
    )

    end_date = models.DateField(
        null=True,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    certificate_url = models.URLField(
        blank=True
    )

    class Meta:
        ordering = ["-end_date"]

    def __str__(self):
        return self.name

class VolunteerExperience(models.Model):

    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name="volunteer_experiences"
    )

    organization = models.CharField(
        max_length=200
    )

    role = models.CharField(
        max_length=150
    )

    start_date = models.DateField(
        null=True,
        blank=True
    )

    end_date = models.DateField(
        null=True,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.role} - {self.organization}"