from django.urls import path
from . import views


urlpatterns = [
    path(
        "",
        views.resume_list,
        name="resume_list"
    ),

    path(
        "create/",
        views.resume_create,
        name="create_resume"
    ),

    path(
    "resume/<int:resume_id>/edit/",
    views.resume_edit,
    name="resume_edit"
),
    path(
    "resume/<int:pk>/delete/",
    views.resume_delete,
    name="resume_delete"
),
path(
    "resume/<int:resume_id>/cancel/",
    views.resume_cancel,
    name="resume_cancel"
),
path(
    "resume/<int:resume_id>/education/add/",
    views.education_add,
    name="education_add"
),

path(
    "resume/<int:resume_id>/education/<int:education_id>/delete/",
    views.education_delete,
    name="education_delete"
),
path(
    "resume/<int:resume_id>/experience/add/",
    views.experience_add,
    name="experience_add"
),

path(
    "resume/<int:resume_id>/experience/<int:experience_id>/delete/",
    views.experience_delete,
    name="experience_delete"
),
path(
    "resume/<int:resume_id>/skill/add/",
    views.skill_add,
    name="skill_add"
),

path(
    "resume/<int:resume_id>/skill/<int:skill_id>/delete/",
    views.skill_delete,
    name="skill_delete"
),
path(
    "resume/<int:resume_id>/project/add/",
    views.project_add,
    name="project_add"
),

path(
    "resume/<int:resume_id>/project/<int:project_id>/delete/",
    views.project_delete,
    name="project_delete"
),
path(
    "resume/<int:resume_id>/certification/add/",
    views.certification_add,
    name="certification_add"
),

path(
    "resume/<int:resume_id>/certification/<int:certification_id>/delete/",
    views.certification_delete,
    name="certification_delete"
),
path(
    "resume/<int:resume_id>/achievement/add/",
    views.achievement_add,
    name="achievement_add"
),

path(
    "resume/<int:resume_id>/achievement/<int:achievement_id>/delete/",
    views.achievement_delete,
    name="achievement_delete"
),
path(
    "resume/<int:resume_id>/training/add/",
    views.training_add,
    name="training_add"
),

path(
    "resume/<int:resume_id>/training/<int:training_id>/delete/",
    views.training_delete,
    name="training_delete"
),
path(
    "resume/<int:resume_id>/volunteer/add/",
    views.volunteer_experience_add,
    name="volunteer_experience_add"
),

path(
    "resume/<int:resume_id>/volunteer/<int:volunteer_id>/delete/",
    views.volunteer_experience_delete,
    name="volunteer_experience_delete"
),
path(
    "resume/<int:resume_id>/language/add/",
    views.language_add,
    name="language_add"
),

path(
    "resume/<int:resume_id>/language/<int:language_id>/delete/",
    views.language_delete,
    name="language_delete"
),
]