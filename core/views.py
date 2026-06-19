from django.shortcuts import render


STATS = [
    {"label": "Placements", "value": "91%", "icon": "trending-up", "gradient": "from-pink-500 via-rose-500 to-orange-400"},
    {"label": "Internships", "value": "1,240", "icon": "briefcase", "gradient": "from-cyan-400 via-blue-500 to-indigo-600"},
    {"label": "Companies", "value": "143", "icon": "building-2", "gradient": "from-violet-500 via-purple-500 to-fuchsia-500"},
    {"label": "Students", "value": "4,320", "icon": "graduation-cap", "gradient": "from-emerald-400 via-teal-500 to-cyan-500"},
]

INTERNSHIPS = [
    {"company": "Google", "initial": "G", "role": "Frontend Developer Intern", "location": "Bangalore", "category": "Frontend", "stipend": "Rs. 45,000/month", "gradient": "from-blue-500 via-cyan-500 to-sky-500"},
    {"company": "Microsoft", "initial": "M", "role": "AI/ML Intern", "location": "Hyderabad", "category": "AI/ML", "stipend": "Rs. 60,000/month", "gradient": "from-violet-500 via-purple-500 to-fuchsia-500"},
    {"company": "Adobe", "initial": "A", "role": "UI/UX Design Intern", "location": "Remote", "category": "UI/UX", "stipend": "Rs. 35,000/month", "gradient": "from-pink-500 via-rose-500 to-orange-400"},
    {"company": "Amazon", "initial": "A", "role": "Backend Developer Intern", "location": "Pune", "category": "Backend", "stipend": "Rs. 50,000/month", "gradient": "from-amber-500 via-orange-500 to-yellow-400"},
    {"company": "Netflix", "initial": "N", "role": "Full Stack Intern", "location": "Mumbai", "category": "Frontend", "stipend": "Rs. 55,000/month", "gradient": "from-red-500 via-rose-500 to-pink-500"},
    {"company": "Tesla", "initial": "T", "role": "Data Science Intern", "location": "Remote", "category": "AI/ML", "stipend": "Rs. 70,000/month", "gradient": "from-emerald-400 via-teal-500 to-cyan-500"},
]

METRICS = [
    {"label": "Placement Success", "value": "91%", "width": "w-[91%]", "gradient": "from-pink-500 to-purple-500", "text": "from-pink-400 to-purple-400"},
    {"label": "Internship Conversion", "value": "74%", "width": "w-[74%]", "gradient": "from-cyan-400 to-blue-500", "text": "from-cyan-400 to-blue-500"},
]


def dashboard(request):
    context = {
        "stats": STATS,
        "filters": ["All", "Frontend", "AI/ML", "UI/UX", "Backend"],
        "internships": INTERNSHIPS,
        "metrics": METRICS,
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
        "activities": [
            "Applied for Google Internship",
            "Resume updated successfully",
            "AI suggested 3 new opportunities",
            "Attendance synced",
        ],
    }
    return render(request, 'dashboard/dashboard.html', context)
