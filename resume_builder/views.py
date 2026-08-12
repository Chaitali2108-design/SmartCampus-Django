from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import (
    Resume,
    PersonalInformation,
    Education,
    Experience,
    Skill,
    Project,
    Certification,
    Achievement,
    Language,
    Training,
    VolunteerExperience,
)

@login_required
def resume_list(request):

    resumes = Resume.objects.filter(
        user=request.user
    ).order_by("-updated_at")

    return render(
        request,
        "resume_builder/resume_list.html",
        {
            "resumes": resumes
        }
    )


@login_required
def resume_create(request):

    if request.method == "POST":

        title = request.POST.get(
            "title",
            "My Resume"
        ).strip()

        template = request.POST.get(
            "template",
            "professional"
        )

        resume = Resume.objects.create(
            user=request.user,
            title=title,
            template=template
        )

        PersonalInformation.objects.create(
            resume=resume,
            full_name=(
                request.user.get_full_name()
                or request.user.username
            ),
            email=request.user.email
        )

        return redirect(
            "resume_edit",
            resume_id=resume.id
        )

    return render(
        request,
        "resume_builder/create_resume.html"
    )


@login_required
def resume_edit(request, resume_id):

    resume = get_object_or_404(
        Resume,
        id=resume_id,
        user=request.user
    )

    try:
        personal_info = resume.personal_information

    except PersonalInformation.DoesNotExist:

        personal_info = PersonalInformation(
            resume=resume,
            full_name=(
                request.user.get_full_name()
                or request.user.username
            ),
            email=request.user.email
        )

    if request.method == "POST":

        # =====================================================
        # PERSONAL INFORMATION
        # =====================================================

        personal_info.full_name = request.POST.get(
            "full_name",
            ""
        ).strip()

        personal_info.professional_title = request.POST.get(
            "professional_title",
            ""
        ).strip()

        personal_info.email = request.POST.get(
            "email",
            ""
        ).strip()

        personal_info.phone = request.POST.get(
            "phone",
            ""
        ).strip()

        personal_info.location = request.POST.get(
            "location",
            ""
        ).strip()

        personal_info.linkedin = request.POST.get(
            "linkedin",
            ""
        ).strip()

        personal_info.github = request.POST.get(
            "github",
            ""
        ).strip()

        personal_info.portfolio = request.POST.get(
            "portfolio",
            ""
        ).strip()

        personal_info.summary = request.POST.get(
            "summary",
            ""
        ).strip()

        if "profile_photo" in request.FILES:

            personal_info.profile_photo = (
                request.FILES["profile_photo"]
            )

        personal_info.save()


        # =====================================================
        # EDUCATION
        # =====================================================

        education_count = int(
            request.POST.get(
                "education_count",
                0
            )
        )

        # Remove old education records
        # before saving the submitted ones.
        resume.education.all().delete()

        for i in range(education_count):

            institution = request.POST.get(
                f"education_{i}_institution",
                ""
            ).strip()

            degree = request.POST.get(
                f"education_{i}_degree",
                ""
            ).strip()

            # Ignore completely empty education blocks
            if not institution and not degree:
                continue

            Education.objects.create(
                resume=resume,

                institution=institution,

                degree=degree,

                field_of_study=request.POST.get(
                    f"education_{i}_field_of_study",
                    ""
                ).strip(),

                start_date=request.POST.get(
                    f"education_{i}_start_date"
                ) or None,

                end_date=request.POST.get(
                    f"education_{i}_end_date"
                ) or None,

                currently_studying=(
                    f"education_{i}_currently_studying"
                    in request.POST
                ),

                grade=request.POST.get(
                    f"education_{i}_grade",
                    ""
                ).strip(),

                description=request.POST.get(
                    f"education_{i}_description",
                    ""
                ).strip(),
            )


        # =====================================================
        # GENERATE / PREVIEW
        # =====================================================

        return redirect(
            "resume_edit",
            resume_id=resume.id
        )


    return render(
        request,
        "resume_builder/resume_edit.html",
        {
            "resume": resume,
            "personal_information": personal_info,
        }
    )


@login_required
def resume_delete(request, pk):

    resume = get_object_or_404(
        Resume,
        pk=pk,
        user=request.user
    )

    if request.method == "POST":

        resume.delete()

        return redirect(
            "resume_list"
        )

    return redirect(
        "resume_edit",
        resume_id=resume.pk
    )


@login_required
def resume_cancel(request, resume_id):

    resume = get_object_or_404(
        Resume,
        id=resume_id,
        user=request.user
    )

    resume.delete()

    return redirect(
        "resume_list"
    )


@login_required
def education_add(request, resume_id):

    resume = get_object_or_404(
        Resume,
        id=resume_id,
        user=request.user
    )

    if request.method == "POST":

        institution = request.POST.get(
            "institution",
            ""
        ).strip()

        degree = request.POST.get(
            "degree",
            ""
        ).strip()

        if institution and degree:

            Education.objects.create(
                resume=resume,

                institution=institution,

                degree=degree,

                field_of_study=request.POST.get(
                    "field_of_study",
                    ""
                ).strip(),

                start_date=request.POST.get(
                    "start_date"
                ) or None,

                end_date=request.POST.get(
                    "end_date"
                ) or None,

                currently_studying=(
                    "currently_studying"
                    in request.POST
                ),

                grade=request.POST.get(
                    "grade",
                    ""
                ).strip(),

                description=request.POST.get(
                    "description",
                    ""
                ).strip(),
            )

    return redirect(
        "resume_edit",
        resume_id=resume.id
    )


@login_required
def education_delete(request, resume_id, education_id):

    resume = get_object_or_404(
        Resume,
        id=resume_id,
        user=request.user
    )

    education = get_object_or_404(
        Education,
        id=education_id,
        resume=resume
    )

    if request.method == "POST":

        education.delete()

    return redirect(
        "resume_edit",
        resume_id=resume.id
    )

@login_required
def experience_add(request, resume_id):

    resume = get_object_or_404(
        Resume,
        id=resume_id,
        user=request.user
    )

    if request.method == "POST":

        company = request.POST.get(
            "company", ""
        ).strip()

        job_title = request.POST.get(
            "job_title", ""
        ).strip()

        if company and job_title:

            Experience.objects.create(
                resume=resume,

                experience_type=request.POST.get(
                    "experience_type",
                    "full_time"
                ),

                company=company,

                job_title=job_title,

                location=request.POST.get(
                    "location",
                    ""
                ).strip(),

                start_date=request.POST.get(
                    "start_date"
                ) or None,

                end_date=request.POST.get(
                    "end_date"
                ) or None,

                currently_working=(
                    "currently_working" in request.POST
                ),

                description=request.POST.get(
                    "description",
                    ""
                ).strip(),
            )

    return redirect(
        "resume_edit",
        resume_id=resume.id
    )


@login_required
def experience_delete(request, resume_id, experience_id):

    resume = get_object_or_404(
        Resume,
        id=resume_id,
        user=request.user
    )

    experience = get_object_or_404(
        Experience,
        id=experience_id,
        resume=resume
    )

    if request.method == "POST":
        experience.delete()

    return redirect(
        "resume_edit",
        resume_id=resume.id
    )

@login_required
def skill_add(request, resume_id):

    resume = get_object_or_404(
        Resume,
        id=resume_id,
        user=request.user
    )

    if request.method == "POST":

        name = request.POST.get(
            "name", ""
        ).strip()

        if name:

            Skill.objects.create(
                resume=resume,
                name=name,
                level=request.POST.get(
                    "level", ""
                ).strip(),
            )

    return redirect(
        "resume_edit",
        resume_id=resume.id
    )


@login_required
def skill_delete(request, resume_id, skill_id):

    resume = get_object_or_404(
        Resume,
        id=resume_id,
        user=request.user
    )

    skill = get_object_or_404(
        Skill,
        id=skill_id,
        resume=resume
    )

    if request.method == "POST":
        skill.delete()

    return redirect(
        "resume_edit",
        resume_id=resume.id
    )

@login_required
def project_add(request, resume_id):

    resume = get_object_or_404(
        Resume,
        id=resume_id,
        user=request.user
    )

    if request.method == "POST":

        name = request.POST.get(
            "name", ""
        ).strip()

        description = request.POST.get(
            "description", ""
        ).strip()

        if name and description:

            Project.objects.create(
                resume=resume,

                name=name,

                role=request.POST.get(
                    "role", ""
                ).strip(),

                description=description,

                technologies=request.POST.get(
                    "technologies", ""
                ).strip(),

                project_url=request.POST.get(
                    "project_url", ""
                ).strip(),

                github_url=request.POST.get(
                    "github_url", ""
                ).strip(),

                start_date=request.POST.get(
                    "start_date"
                ) or None,

                end_date=request.POST.get(
                    "end_date"
                ) or None,

                is_current=(
                    "is_current" in request.POST
                ),
            )

    return redirect(
        "resume_edit",
        resume_id=resume.id
    )


@login_required
def project_delete(request, resume_id, project_id):

    resume = get_object_or_404(
        Resume,
        id=resume_id,
        user=request.user
    )

    project = get_object_or_404(
        Project,
        id=project_id,
        resume=resume
    )

    if request.method == "POST":
        project.delete()

    return redirect(
        "resume_edit",
        resume_id=resume.id
    )

@login_required
def certification_add(request, resume_id):

    resume = get_object_or_404(
        Resume,
        id=resume_id,
        user=request.user
    )

    if request.method == "POST":

        name = request.POST.get(
            "name", ""
        ).strip()

        if name:

            Certification.objects.create(
                resume=resume,

                name=name,

                issuing_organization=request.POST.get(
                    "issuing_organization",
                    ""
                ).strip(),

                issue_date=request.POST.get(
                    "issue_date"
                ) or None,

                credential_id=request.POST.get(
                    "credential_id",
                    ""
                ).strip(),

                credential_url=request.POST.get(
                    "credential_url",
                    ""
                ).strip(),
            )

    return redirect(
        "resume_edit",
        resume_id=resume.id
    )


@login_required
def certification_delete(
    request,
    resume_id,
    certification_id
):

    resume = get_object_or_404(
        Resume,
        id=resume_id,
        user=request.user
    )

    certification = get_object_or_404(
        Certification,
        id=certification_id,
        resume=resume
    )

    if request.method == "POST":
        certification.delete()

    return redirect(
        "resume_edit",
        resume_id=resume.id
    )

@login_required
def achievement_add(request, resume_id):

    resume = get_object_or_404(
        Resume,
        id=resume_id,
        user=request.user
    )

    if request.method == "POST":

        title = request.POST.get(
            "title",
            ""
        ).strip()

        if title:

            Achievement.objects.create(
                resume=resume,
                title=title,
                description=request.POST.get(
                    "description",
                    ""
                ).strip(),
                date=request.POST.get(
                    "date"
                ) or None,
            )

    return redirect(
        "resume_edit",
        resume_id=resume.id
    )


@login_required
def achievement_delete(request, resume_id, achievement_id):

    resume = get_object_or_404(
        Resume,
        id=resume_id,
        user=request.user
    )

    achievement = get_object_or_404(
        Achievement,
        id=achievement_id,
        resume=resume
    )

    if request.method == "POST":
        achievement.delete()

    return redirect(
        "resume_edit",
        resume_id=resume.id
    )

@login_required
def training_add(request, resume_id):

    resume = get_object_or_404(
        Resume,
        id=resume_id,
        user=request.user
    )

    if request.method == "POST":

        name = request.POST.get(
            "name",
            ""
        ).strip()

        if name:

            Training.objects.create(
                resume=resume,

                name=name,

                organization=request.POST.get(
                    "organization",
                    ""
                ).strip(),

                start_date=request.POST.get(
                    "start_date"
                ) or None,

                end_date=request.POST.get(
                    "end_date"
                ) or None,

                description=request.POST.get(
                    "description",
                    ""
                ).strip(),

                certificate_url=request.POST.get(
                    "certificate_url",
                    ""
                ).strip(),
            )

    return redirect(
        "resume_edit",
        resume_id=resume.id
    )


@login_required
def training_delete(
    request,
    resume_id,
    training_id
):

    resume = get_object_or_404(
        Resume,
        id=resume_id,
        user=request.user
    )

    training = get_object_or_404(
        Training,
        id=training_id,
        resume=resume
    )

    if request.method == "POST":
        training.delete()

    return redirect(
        "resume_edit",
        resume_id=resume.id
    )

@login_required
def volunteer_experience_add(request, resume_id):

    resume = get_object_or_404(
        Resume,
        id=resume_id,
        user=request.user
    )

    if request.method == "POST":

        organization = request.POST.get(
            "organization",
            ""
        ).strip()

        role = request.POST.get(
            "role",
            ""
        ).strip()

        if organization and role:

            VolunteerExperience.objects.create(
                resume=resume,

                organization=organization,

                role=role,

                start_date=request.POST.get(
                    "start_date"
                ) or None,

                end_date=request.POST.get(
                    "end_date"
                ) or None,

                description=request.POST.get(
                    "description",
                    ""
                ).strip(),
            )

    return redirect(
        "resume_edit",
        resume_id=resume.id
    )


@login_required
def volunteer_experience_delete(
    request,
    resume_id,
    volunteer_id
):

    resume = get_object_or_404(
        Resume,
        id=resume_id,
        user=request.user
    )

    volunteer = get_object_or_404(
        VolunteerExperience,
        id=volunteer_id,
        resume=resume
    )

    if request.method == "POST":
        volunteer.delete()

    return redirect(
        "resume_edit",
        resume_id=resume.id
    )

@login_required
def language_add(request, resume_id):

    resume = get_object_or_404(
        Resume,
        id=resume_id,
        user=request.user
    )

    if request.method == "POST":

        name = request.POST.get(
            "name",
            ""
        ).strip()

        if name:

            Language.objects.create(
                resume=resume,
                name=name,
                proficiency=request.POST.get(
                    "proficiency",
                    ""
                ).strip(),
            )

    return redirect(
        "resume_edit",
        resume_id=resume.id
    )


@login_required
def language_delete(
    request,
    resume_id,
    language_id
):

    resume = get_object_or_404(
        Resume,
        id=resume_id,
        user=request.user
    )

    language = get_object_or_404(
        Language,
        id=language_id,
        resume=resume
    )

    if request.method == "POST":
        language.delete()

    return redirect(
        "resume_edit",
        resume_id=resume.id
    )