from django.urls import path

from home.views import WelcomeView, HomeView

app_name = 'home'

urlpatterns = [
    path("", WelcomeView.as_view(), name="welcome"),
    path("home/", HomeView.as_view(), name="home")

]
