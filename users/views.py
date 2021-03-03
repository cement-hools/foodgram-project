from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('login')  # где login — это параметр "name" в path()
    template_name = 'signup.html'
