from django.shortcuts import render
from django.views.generic import TemplateView

from account.models import UserProfile


# Create your views here.
class WelcomeView(TemplateView):
    template_name = 'home/welcome.html'


class HomeView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user_profile = UserProfile.objects.get(pk=self.request.user.pk)
            context['user_profile'] = user_profile
        return context
