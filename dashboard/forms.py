from django import forms
from .models import StudentProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "w-full bg-black/20 border border-white/10 rounded-2xl px-5 py-4 text-white placeholder-slate-400 outline-none focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/30",
                "placeholder": "Username"
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full bg-black/20 border border-white/10 rounded-2xl px-5 py-4 text-white placeholder-slate-400 outline-none",
                "placeholder": "Password",
            }
        )
    )



class SignupForm(UserCreationForm):

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "w-full bg-black/20 border border-white/10 rounded-2xl px-5 py-4 text-white placeholder-slate-400 outline-none focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/30",
                "placeholder": "Email Address",
            }
        )
    )

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "w-full bg-black/20 border border-white/10 rounded-2xl px-5 py-4 text-white placeholder-slate-400 outline-none focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/30",
                "placeholder": "Username",
            }
        )
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full bg-black/20 border border-white/10 rounded-2xl px-5 py-4 text-white placeholder-slate-400 outline-none focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/30",
                "placeholder": "Password",
            }
        )
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full bg-black/20 border border-white/10 rounded-2xl px-5 py-4 text-white placeholder-slate-400 outline-none focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/30",
                "placeholder": "Confirm Password",
            }
        )
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class StudentProfileForm(forms.ModelForm):

    class Meta:

        model = StudentProfile

        fields = [
            "full_name",
            "college",
            "branch",
            "year",
            "skills",
            "bio",
            "github",
            "linkedin",
            "phone",
            "location",
            "profile_photo",
            "resume",
        ]

        widgets = {

            "full_name": forms.TextInput(attrs={
                "class": "profile-input",
                "placeholder": "Full Name",
                
            }),

            "college": forms.TextInput(attrs={
                "class": "profile-input",
                "placeholder": "College"
            }),

            "branch": forms.TextInput(attrs={
                "class": "profile-input",
                "placeholder": "Branch"
            }),

            "year": forms.TextInput(attrs={
                "class": "profile-input",
                "placeholder": "Year"
            }),

            "skills": forms.TextInput(attrs={
                "class": "profile-input",
                "placeholder": "Skills (comma separated)"
            }),

            "bio": forms.Textarea(attrs={
                "class": "profile-input min-h-[140px]",
                "placeholder": "Career Bio"
            }),

            "github": forms.URLInput(attrs={
                "class": "profile-input",
                "placeholder": "GitHub URL"
            }),

            "linkedin": forms.URLInput(attrs={
                "class": "profile-input",
                "placeholder": "LinkedIn URL"
            }),

            "phone": forms.TextInput(attrs={
                "class": "profile-input",
                "placeholder": "Phone Number"
            }),

            "location": forms.TextInput(attrs={
                "class": "profile-input",
                "placeholder": "Location"
            }),
        }

class RoadmapForm(forms.Form):

    current_skills = forms.CharField(
        widget=forms.Textarea
    )

    target_role = forms.CharField(
        max_length=100
    )