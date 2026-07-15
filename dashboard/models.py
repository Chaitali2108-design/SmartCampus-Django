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

#for job preparations page

class Question(models.Model):
    TEST_TYPES = [
        ("aptitude", "Aptitude"),
        ("technical", "Technical"),
    ]

    SECTION_CHOICES = [
        ("quantitative", "Quantitative Aptitude"),
        ("logical", "Logical Reasoning"),
        ("verbal", "Verbal Ability"),
        ("os", "Operating Systems"),
        ("dbms", "Database Management System"),
        ("cn", "Computer Networks"),
        ("oops", "Object-Oriented Programming"),
        ("dsa", "Data Structures & Algorithms"),
        ("sql", "SQL"),
        ("java", "Java"),
        ("software", "Software Engineering"),
    ]

    DIFFICULTY = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    ]

    test_type = models.CharField(max_length=20, choices=TEST_TYPES)
    section = models.CharField(max_length=50, choices=SECTION_CHOICES)

    question = models.TextField()

    option_a = models.CharField(max_length=500)
    option_b = models.CharField(max_length=500)
    option_c = models.CharField(max_length=500)
    option_d = models.CharField(max_length=500)

    correct_option = models.CharField(max_length=1)

    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY,
        default="medium",
    )

    marks = models.PositiveSmallIntegerField(default=1)

    negative_marks = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0,
    )

    question_image = models.ImageField(
    upload_to="questions/",
    blank=True,
    null=True
    )

    code_snippet = models.TextField(
    blank=True,
    default=""
    )

    explanation = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question[:60]
    

class TestAttempt(models.Model):
    STATUS_CHOICES = [
        ("in_progress", "In Progress"),
        ("submitted", "Submitted"),
    ]

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="test_attempts"
    )

    test_type = models.CharField(
        max_length=20,
        choices=Question.TEST_TYPES
    )

    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(blank=True, null=True)

    total_questions = models.PositiveIntegerField(default=0)
    score = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="in_progress"
    )

    def __str__(self):
        return f"{self.student.full_name} - {self.test_type}"
    

class StudentAnswer(models.Model):
    OPTION_CHOICES = [
        ("A", "Option A"),
        ("B", "Option B"),
        ("C", "Option C"),
        ("D", "Option D"),
    ]

    attempt = models.ForeignKey(
        TestAttempt,
        on_delete=models.CASCADE,
        related_name="answers"
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )

    selected_option = models.CharField(
        max_length=1,
        choices=OPTION_CHOICES,
        blank=True,
        default=""
    )

    marked_for_review = models.BooleanField(default=False)

    answered_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("attempt", "question")


#for coding questions

class CodingQuestion(models.Model):
    DIFFICULTY = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    ]

    title = models.CharField(max_length=200)

    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY
    )



    marks = models.IntegerField(default=50)

    statement = models.TextField()

    input_format = models.TextField(blank=True)

    output_format = models.TextField(blank=True)

    constraints = models.TextField(blank=True)

    sample_input = models.TextField(blank=True)

    sample_output = models.TextField(blank=True)

    explanation = models.TextField(blank=True)

    official_input = models.TextField(
    blank=True,
    help_text="Input used during submission evaluation"
)

    expected_output = models.TextField(
    blank=True,
    help_text="Expected output for the official input"
)

    question_image = models.ImageField(
        upload_to="coding_questions/",
        blank=True,
        null=True
    )

    starter_code = models.TextField(
        default="""def solve():
    pass

if __name__ == "__main__":
    solve()
"""
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
#for communication test 
class CommunicationQuestion(models.Model):

    QUESTION_TYPES = [
        ("grammar", "Grammar MCQ"),
        ("listening", "Listening"),
        ("grammar_situation", "Grammar Situation"),
        ("email", "Email Writing"),
        ("expression", "Thought Expression"),
    ]

    question_type = models.CharField(
        max_length=30,
        choices=QUESTION_TYPES
    )

    title = models.CharField(max_length=255)

    question = models.TextField()

    marks = models.IntegerField(default=2)

    # ---------- MCQ ----------
    option1 = models.CharField(max_length=255, blank=True)
    option2 = models.CharField(max_length=255, blank=True)
    option3 = models.CharField(max_length=255, blank=True)
    option4 = models.CharField(max_length=255, blank=True)

    correct_option = models.CharField(
        max_length=1,
        blank=True,
        help_text="A/B/C/D"
    )

    # ---------- Listening ----------
    audio = models.FileField(
        upload_to="communication_audio/",
        blank=True,
        null=True
    )

    expected_answer = models.TextField(blank=True)

    # ---------- Writing ----------
    sample_answer = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.question_type} - {self.title}"