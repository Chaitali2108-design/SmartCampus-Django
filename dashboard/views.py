from django.shortcuts import render, redirect
from .models import Internship
from .models import Metric
from .models import Activity
from .models import PlacementDrive
from .forms import StudentProfileForm
from .models import StudentProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import SignupForm
from django.shortcuts import get_object_or_404
from .models import Application
from django.contrib import messages
from django.http import JsonResponse
from .models import InternshipApplication
from .models import InternshipOpportunity
from django.db.models import Count



#for recruiter dashboard

def recruiter_dashboard(request):

    internships = InternshipOpportunity.objects.all()


    applications = InternshipApplication.objects.select_related(
    "user",
    "internship"
    ).order_by("-applied_at")

    context = {

    "total_jobs": internships.count(),

    "total_applications": applications.count(),

    "active_jobs": internships.count(),

    "trending_jobs": internships.filter(
        trending=True
    ).count(),

    "recent_applications": applications[:6],

}

    return render(
        request,
        "recruiter/recruiter_dashboard.html",
        context,
    )


#For dashboard section
from .models import KPI

stats = KPI.objects.all()


metrics = Metric.objects.all()

activities = Activity.objects.order_by("-created_at")[:5]

#for placement page
drives = PlacementDrive.objects.all()

pipeline = [
    {"stage": "Applications", "value": "1.4K", "width": "92%"},
    {"stage": "Shortlisted", "value": "860", "width": "74%"},
    {"stage": "Interviews", "value": "420", "width": "51%"},
    {"stage": "Selected", "value": "214", "width": "36%"},
]

@login_required
def dashboard(request):
    internships = Internship.objects.all()

    context = {
        "stats": stats,
        "filters": ["All",  "Software", "Cloud", "Data Science", "AI","Cyber Security","Management",],
        "internships": internships,
        "metrics": metrics,
        "suggestions": [
            "How can I improve my resume?",
            "Best internships for frontend developers",
            "Top AI/ML companies hiring now",
            "Tips to crack placement interviews",
        ],
        "recommendations": [
            "Frontend Developer Internship",
            "AI/ML Bootcamp Program",
            "Resume Improvement Suggestions",
            "Top Companies Hiring This Week",
        ],
        "activities":activities
    }
    return render(request, 'dashboard/dashboard.html', context)

from openai import OpenAI
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

client = OpenAI(
    api_key=settings.GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

@login_required
def placements(request):

    roadmap = ""
    roadmap_steps = request.session.pop(
        "roadmap_steps",
        []
    )

    if request.method == "POST":

        skills = request.POST.get("skills")
        role = request.POST.get("role")

        prompt = f"""
Current Skills: {skills}

Target Role: {role}

Generate a concise career roadmap.

Rules:
- Exactly 8 roadmap steps.
- Each step must contain only a short title.
- Maximum 6 words per step.
- No explanations.
- No phases.
- No paragraphs.
- No recommendations.
- No markdown.
"""

        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            roadmap = response.choices[0].message.content

            roadmap_steps = [
                step.strip()
                for step in roadmap.split("\n")
                if step.strip()
            ]

            request.session["roadmap_steps"] = roadmap_steps

            return redirect("placements")

        except Exception as e:
            roadmap = f"Error: {e}"

    context = {
        "drives": drives,
        "pipeline": pipeline,
        "roadmap": roadmap,
        "roadmap_steps": roadmap_steps,
    }

    return render(
        request,
        "placements/placements.html",
        context
    )

#for profile

@login_required
def profile(request):

    profile, created = StudentProfile.objects.get_or_create(
        user=request.user
    )
    applied_jobs = Application.objects.filter(
    student=profile
    ).count()
    if request.method == "POST":

        form = StudentProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():

            form.save()

    else:

        form = StudentProfileForm(
            instance=profile
        )

    readiness = 0

    if profile.full_name:
        readiness += 10

    if profile.college:
        readiness += 10

    if profile.branch:
        readiness += 10

    if profile.year:
        readiness += 10

    if profile.skills:
        readiness += 15

    if profile.bio:
        readiness += 10

    if profile.github:
        readiness += 10

    if profile.linkedin:
        readiness += 10

    if profile.resume:
        readiness += 15

    return render(
        request,
        "profile/profile.html",
        {
            "form": form,
            "profile": profile,
            "readiness": readiness,
            "applied_jobs": applied_jobs,
        }
    )


def landing(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    return render(request, "landing.html")




def signup(request):

    if request.method == "POST":

        form = SignupForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect("dashboard")

    else:

        form = SignupForm()

    return render(
        request,
        "registration/signup.html",
        {"form": form}
    )

#for placement apply job button
@login_required
def apply_job(request, pk):

    profile = StudentProfile.objects.get(
        user=request.user
    )

    placement = get_object_or_404(
        PlacementDrive,
        id=pk
    )

    application, created = Application.objects.get_or_create(
        student=profile,
        placement=placement
    )

    if created:

        return JsonResponse({
            "status": "success",
            "message": f"Successfully applied for {placement.company}"
        })

    return JsonResponse({
        "status": "warning",
        "message": f"Already applied for {placement.company}"
    })


@login_required
def my_applications(request):

    profile, created = StudentProfile.objects.get_or_create(
        user=request.user
    )

    applications = Application.objects.filter(
        student=profile
    ).select_related("placement")

    internship_applications = InternshipApplication.objects.filter(
        user=request.user
    ).select_related("internship")

    return render(
        request,
        "placements/my_applications.html",
        {
            "applications": applications,
            "internship_applications": internship_applications,
        }
    )

from openai import OpenAI
from django.conf import settings

client = OpenAI(
    api_key=settings.GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

def ai_roadmap(request):
    roadmap = ""

    if request.method == "POST":
        skills = request.POST.get("skills")
        role = request.POST.get("role")

        prompt = f"""
        Current Skills: {skills}

        Target Role: {role}

        Create a step-by-step learning roadmap.
        """

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        roadmap = response.choices[0].message.content

    return render(
        request,
        "roadmap/roadmap.html",
        {"roadmap": roadmap}
    )

#for internship page 


@login_required
def internships(request):
    query = request.GET.get("q", "").strip()
    location = request.GET.get("location", "").strip()

    internships = InternshipOpportunity.objects.all().order_by("-created_at")

    if query:
        internships = internships.filter(
            models.Q(role__icontains=query)
            | models.Q(company__icontains=query)
            | models.Q(skills__icontains=query)
        )

    if location and location != "All Locations":
        internships = internships.filter(location__icontains=location)

    for internship in internships:
        internship.skills_list = [
            skill.strip()
            for skill in internship.skills.split(",")
            if skill.strip()
        ]

    all_internships = InternshipOpportunity.objects.all()
    remote_count = all_internships.filter(location__icontains="Remote").count()
    company_count = all_internships.values("company").distinct().count()

    return render(
        request,
        "internships/internships.html",
        {
            "internships": internships,
            "stats": [
                {"title": "Open Roles", "value": all_internships.count()},
                {"title": "Remote Jobs", "value": remote_count},
                {"title": "Companies", "value": company_count},
                {"title": "Highest Stipend", "value": "&#8377;70K"},
            ],
            "categories": ["Frontend", "AI / ML", "UI / UX", "Backend"],
            "top_companies": ["Google", "Microsoft", "Amazon", "Adobe", "Netflix"],
            "tips": [
                {
                    "title": "Build Strong Resume",
                    "desc": "Keep projects, skills, and achievements updated.",
                },
                {
                    "title": "Optimize LinkedIn",
                    "desc": "Create a professional profile and stay active.",
                },
                {
                    "title": "Practice Interviews",
                    "desc": "Prepare aptitude, coding, and communication skills.",
                },
                {
                    "title": "Create Projects",
                    "desc": "Real-world projects increase hiring chances.",
                },
            ],
            "query": query,
            "selected_location": location,
        }
    )


@login_required
def apply_internship(request, pk):
    internship = get_object_or_404(InternshipOpportunity, id=pk)

    if request.method != "POST":
        return redirect("internships")

    application, created = InternshipApplication.objects.get_or_create(
        user=request.user,
        internship=internship,
    )

    if created:
        messages.success(
            request,
            f"Successfully applied for {internship.company}",
        )
    else:
        messages.warning(
            request,
            f"Already applied for {internship.company}",
        )

    return redirect("internships")


#preparation page

@login_required
def preparation(request):
    rounds = [
        {
            "id": 1,
            "title": "Aptitude Test",
            "description": "Quantitative, Logical & Verbal",
            "questions": 25,
            "duration": "30 mins",
            "icon": "brain",
            "color": "from-pink-500 to-pink-600",
            "test_type": "aptitude",
        },
        {
            "id": 2,
            "title": "Technical MCQs",
            "description": "OS, DBMS, CN, OOP",
            "questions": 30,
            "duration": "40 mins",
            "icon": "cpu",
            "color": "from-violet-500 to-purple-600",
            "test_type": "technical",
        },
        {
            "id": 3,
            "title": "Coding Challenge",
            "description": "Programming Problems",
            "questions": 3,
            "duration": "60 mins",
            "icon": "code",
            "color": "from-cyan-500 to-blue-500",
            "test_type": "coding",
        },
        {
            "id": 4,
            "title": "Communication Test",
            "description": "Communication & Ideas",
            "questions": 1,
            "duration": "20 mins",
            "icon": "users",
            "color": "from-orange-500 to-amber-500",
            "test_type": "communication",
        },
        {
            "id": 5,
            "title": "HR Interview",
            "description": "Core Subject Questions",
            "questions": 20,
            "duration": "45 mins",
            "icon": "message-square",
            "color": "from-emerald-500 to-green-500",
            "test_type": "hr",
        },
        {
            "id": 6,
            "title": "Logical Reasoning",
            "test_type": "logical",
           "description": "Behavioral Questions",
            "questions": 15,
            "duration": "25 mins",
            "icon": "briefcase",
            "color": "from-indigo-500 to-indigo-700",
        },
        {
            "id": 7,
            "title": "Quantitative Aptitude",
            "test_type": "quantitative",
            "description": "TCS, Infosys, Google & More",
            "questions": 50,
            "duration": "90 mins",
            "icon": "building-2",
            "color": "from-rose-500 to-red-500",
        },
    ]

    return render(
        request,
        "preparation/index.html",
        {"rounds": rounds},
    )
#for tests
def preparation_test(request, test_type):
    return render(request, "preparation/test.html", {
        "test_type": test_type
    })

#for result of test
import json
from django.http import JsonResponse

def preparation_result(request):

    if request.method == "POST":

        data = json.loads(request.body)

        request.session["result"] = data

        return JsonResponse({"success":True})

    return render(
        request,
        "preparation/result.html",
        {
            "result":request.session.get("result",{})
        }
    )