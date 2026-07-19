from django.contrib import admin
from .models import Internship, PlacementDrive
from .models import Application
from .models import InternshipOpportunity, InternshipApplication

from .models import CommunicationQuestion



admin.site.register(Internship)
admin.site.register(PlacementDrive)
admin.site.register(Application)
admin.site.register(InternshipOpportunity)
admin.site.register(InternshipApplication)



from .models import Question, TestAttempt, StudentAnswer


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "test_type",
        "section",
        "difficulty",
        "marks",
    )

    list_filter = (
        "test_type",
        "section",
        "difficulty",
    )

    search_fields = (
        "question",
    )


@admin.register(TestAttempt)
class TestAttemptAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "student",
        "test_type",
        "status",
        "score",
        "started_at",
    )

    list_filter = (
        "test_type",
        "status",
    )

    search_fields = (
        "student__full_name",
    )


@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = (
        "attempt",
        "question",
        "selected_option",
        "marked_for_review",
    )

    list_filter = (
        "marked_for_review",
    )

from .models import CodingQuestion


@admin.register(CodingQuestion)
class CodingQuestionAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "difficulty",
        "marks",
    )

    list_filter = (
        "difficulty",
    )

    search_fields = (
        "title",
    )

@admin.register(CommunicationQuestion)
class CommunicationQuestionAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "question_type",
        "difficulty",
        "marks",
        "correct_option",
    )

    list_filter = (
        "question_type",
        "difficulty",
    )