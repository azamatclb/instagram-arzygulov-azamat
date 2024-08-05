from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView

from account.foms import UserRegistrationForm, SearchForm
from account.models import Profile
from webapp.models import Post

# Create your views here.


User = get_user_model()


def login_view(request):
    context = {}
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('webapp:posts')
        else:
            context["has_error"] = True
    return render(request, 'login.html', context=context)


def logout_view(request):
    logout(request)
    return redirect('webapp:posts')


class RegisterView(CreateView):
    template_name = 'registration.html'
    form_class = UserRegistrationForm
    model = User

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next_url:
            next_url = self.request.POST.get('next')
        if not next_url:
            next_url = reverse('webapp:posts')
        return next_url


class ProfileView(LoginRequiredMixin, DetailView):
    template_name = 'profile_view.html'
    model = Profile
    context_object_name = 'user_obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.object
        posts = Post.objects.filter(author=profile)
        context['posts'] = posts
        context['posts_count'] = posts.count()
        context['followers_count'] = profile.followers_count
        context['following_count'] = profile.following_count
        return context


class ProfileList(ListView):
    template_name = 'profiles_list.html'
    model = Profile
    context_object_name = 'profiles'

    def dispatch(self, request, *args, **kwargs):
        self.form = self.get_form()
        self.search_value = self.get_search_value()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            queryset = queryset.filter(
                Q(username__icontains=self.search_value) | Q(email__icontains=self.search_value) | Q(
                    first_name__icontains=self.search_value)
            )
        return queryset

    def get_form(self):
        return SearchForm(self.request.GET)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.form
        context['search_value'] = self.search_value
        return context

    def get_search_value(self):
        form = self.form
        if form.is_valid():
            return form.cleaned_data['search']
        return form
