from django.contrib.auth.views import LoginView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.urls import path

from account import views
from account.views import (
    TeamCreateView,
    TeamListView,
    TeamDetailView,
    TeamUpdateView,
    TeamDeleteView,
    SignUpView,
    UserProfileListView,
    UserProfileDetailView,
    UserProfileCreateView,
    UserProfileUpdateView,
    UserProfileDeleteView, LogoutView, CustomLoginView,
)
from room_reservation import settings

app_name = "account"

urlpatterns = [
                  path("teams/", TeamListView.as_view(), name="team_list"),
                  path("teams/<int:pk>/", TeamDetailView.as_view(), name="team_detail"),
                  path("teams/create/", TeamCreateView.as_view(), name="team_create"),
                  path("teams/update/<int:pk>/", TeamUpdateView.as_view(), name="team_update"),
                  path("teams/delete/<int:pk>/", TeamDeleteView.as_view(), name="team_delete"),
                  path('signup/', SignUpView.as_view(), name='signup'),
                  path('verify/', views.UserSignUpVerifyCodeView.as_view(), name='verify_code'),
                  path('login/', CustomLoginView.as_view(), name='login'),
                  path('login_verify/', views.UserLoginVerifyCodeView.as_view(), name='verify_login_code'),
                  path('logout/', LogoutView.as_view(), name='logout'),
                  path("user_profiles/", UserProfileListView.as_view(), name="user_profile_list"),
                  path("user_profiles/<int:pk>/", UserProfileDetailView.as_view(), name="user_profile_detail"),
                  path("user_profiles/create/", UserProfileCreateView.as_view(), name="user_profile_create"),
                  path("user_profiles/update/<int:pk>/", UserProfileUpdateView.as_view(), name="user_profile_update"),
                  path("user_profiles/delete/<int:pk>/", UserProfileDeleteView.as_view(), name="user_profile_delete"),
              ]
