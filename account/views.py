import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    FormView,
)

from account.forms import (
    SignUpForm,
    VerifyCodeForm,
    TeamForm,
    UserProfileForm,
    CustomLoginForm,
    UserProfileUpdateForm,
)
from account.models import Team, OTP, UserProfile, MobileOTP
from account.permissions import (
    AdminMixin,
    OwnerOrAdminMixin,
    TeamMemberOrManagerOrAdminMixin,
    TeamManagerOrAdminMixin,
)
from utils import send_otp_sms, send_otp_email


class TeamDetailView(LoginRequiredMixin, TeamMemberOrManagerOrAdminMixin, DetailView):
    model = Team
    context_object_name = "teams"
    template_name = "account/team_detail.html"


class TeamListView(LoginRequiredMixin, AdminMixin, ListView):
    model = Team
    context_object_name = "teams"
    template_name = "account/team_list.html"


class TeamCreateView(LoginRequiredMixin, AdminMixin, CreateView):
    model = Team
    form_class = TeamForm
    template_name = "account/team_form.html"
    success_url = reverse_lazy("account:team_list")


class TeamUpdateView(LoginRequiredMixin, TeamManagerOrAdminMixin, UpdateView):
    model = Team
    form_class = TeamForm
    context_object_name = "team"
    template_name = "account/team_form.html"
    success_url = reverse_lazy("account:team_list")


class TeamDeleteView(LoginRequiredMixin, AdminMixin, DeleteView):
    model = Team
    context_object_name = "team"
    template_name = "account/team_delete.html"
    success_url = reverse_lazy("account:team_list")


class UserProfileDetailView(LoginRequiredMixin, OwnerOrAdminMixin, DetailView):
    model = UserProfile
    context_object_name = "user_profile"
    template_name = "account/user_profile_detail.html"


class UserProfileListView(LoginRequiredMixin, AdminMixin, ListView):
    model = UserProfile
    context_object_name = "user_profiles"
    template_name = "account/user_profile_list.html"


class UserProfileCreateView(CreateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = "account/user_profile_form.html"
    success_url = reverse_lazy("account:user_profile_list")


class UserProfileUpdateView(LoginRequiredMixin, OwnerOrAdminMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileUpdateForm
    template_name = "account/user_profile_update.html"
    success_url = reverse_lazy("home:home")


class UserProfileDeleteView(LoginRequiredMixin, OwnerOrAdminMixin, DeleteView):
    model = UserProfile
    context_object_name = "user_profile"
    template_name = "account/user_profile_delete.html"
    success_url = reverse_lazy("home:home")


class CustomLoginView(View):
    form = CustomLoginForm

    def post(self, request, *args, **kwargs):
        form = self.form(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                user_profile = UserProfile.objects.get(username=username)
                otp_code = random.randint(1000, 9999)
                send_otp_sms(phone=user_profile.phone_number, code=otp_code)
                MobileOTP.objects.create(
                    phone_number=user_profile.phone_number, code=otp_code
                )
                # Save user login info in session
                request.session["userLoginInfo"] = {
                    "username": username,
                    "password": password,
                    "phone_number": user_profile.phone_number,
                }

                return redirect("account:verify_login_code")
            else:
                messages.error(
                    request, "Invalid username or password.", extra_tags="danger"
                )
                return render(request, "account/login.html", {"form": form})

        else:
            messages.error(request, "Invalid form submission.", extra_tags="danger")
            return render(request, "account/login.html", {"form": form})

    def get(self, request, *args, **kwargs):
        form = self.form()
        return render(request, "account/login.html", {"form": form})


class UserLoginVerifyCodeView(View):
    form_class = VerifyCodeForm

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user_login_info = request.session.get("userLoginInfo")
            if user_login_info:
                code_instance = MobileOTP.objects.filter(
                    phone_number=user_login_info["phone_number"]
                ).last()
                if code_instance.code == int(form.cleaned_data["code"]):
                    user = authenticate(
                        username=user_login_info["username"],
                        password=user_login_info["password"],
                    )
                    if user is not None:
                        login(request, user)
                        messages.success(
                            request,
                            "Welcome, you have successfully logged in.",
                            "success",
                        )
                        return redirect("home:home")

                    else:
                        messages.error(
                            request,
                            "Authentication failed. Please try again.",
                            "danger",
                        )
                        return redirect("account:login")
                else:
                    messages.error(request, "Invalid verification code.", "danger")
                    return redirect("account:verify_login_code")
            else:
                messages.error(request, "User login information not found.", "danger")
                return redirect("account:login")
        return redirect("account:login")

    def get(self, request):
        form = self.form_class
        return render(request, "account/verify_login.html", {"form": form})


class SignUpView(View):
    form_class = SignUpForm

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            code = random.randint(1000, 9999)
            OTP.objects.create(email=form.cleaned_data["email"], code=code)
            hashed_password = make_password(form.cleaned_data["password"])
            send_otp_email(email=form.cleaned_data["email"], code=code)
            request.session["userRegistrationInfo"] = {
                "phone": form.cleaned_data["phone_number"],
                "email": form.cleaned_data["email"],
                "username": form.cleaned_data["username"],
                "first_name": form.cleaned_data["first_name"],
                "last_name": form.cleaned_data["last_name"],
                "password": hashed_password,
            }
            messages.success(request, "we send you code :))", "success")
            return redirect("account:verify_code")
        else:
            return render(request, "account/signup.html", {"form": form})

    def get(self, request):
        form = self.form_class
        return render(request, "account/signup.html", {"form": form})


class UserSignUpVerifyCodeView(View):
    form_class = VerifyCodeForm

    def post(self, request):
        user_session = request.session.get("userRegistrationInfo")
        if user_session is None:
            return redirect("home:welcome")

        code_instance = OTP.objects.filter(email=user_session["email"]).last()
        if code_instance is None:
            messages.error(request, "Invalid code. Please try again.", "danger")
            return redirect("account:verify_code")

        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if int(data["code"]) == code_instance.code:
                UserProfile.objects.create(
                    phone_number=user_session["phone"],
                    email=user_session["email"],
                    username=user_session["username"],
                    first_name=user_session["first_name"],
                    last_name=user_session["last_name"],
                    password=user_session["password"],
                )
                code_instance.delete()
                messages.success(
                    request, "Welcome! You have signed up successfully.", "success"
                )
                return redirect("home:home")

            else:
                messages.error(request, "Invalid code. Please try again.", "danger")
                return redirect("account:verify_code")
        else:
            messages.error(request, "Invalid form data.", "danger")
            return redirect("home:welcome")

    def get(self, request):
        form = self.form_class
        return render(request, "account/verify.html", {"form": form})


class LogoutView(View):
    @staticmethod
    def get(request):
        logout(request)
        messages.success(request, "You have been logged out successfully.", "success")
        return redirect("home:welcome")
