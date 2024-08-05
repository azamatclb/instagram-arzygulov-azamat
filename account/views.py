from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, DetailView, ListView

from account.forms import UserRegistrationForm, SearchForm
from account.models import Profile, Subscription
from webapp.models import Post

User = get_user_model()


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
        context['posts'] = Post.objects.filter(author=profile)
        context['posts_count'] = profile.posts_count
        context['followers_count'] = profile.followers_count
        context['following_count'] = profile.following_count
        context['is_subscribed'] = self.request.user.following.filter(id=profile.id).exists()
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
        return None


class SubscribeView(LoginRequiredMixin, View):
    def post(self, request, user_id):
        user_to_subscribe = get_object_or_404(Profile, id=user_id)

        if request.user != user_to_subscribe:
            subscription, created = Subscription.objects.get_or_create(follower=request.user, following=user_to_subscribe)
            if created:
                request.user.following_count += 1
                user_to_subscribe.followers_count += 1
                request.user.save()
                user_to_subscribe.save()

        return HttpResponseRedirect(reverse('account:profile', args=[user_id]))


class UnsubscribeView(LoginRequiredMixin, View):
    def post(self, request, user_id):
        user_to_unfollow = get_object_or_404(Profile, id=user_id)
        if request.user != user_to_unfollow:
            subscription = Subscription.objects.filter(follower=request.user, following=user_to_unfollow).first()

            if subscription:
                subscription.delete()
                request.user.following_count -= 1
                user_to_unfollow.followers_count -= 1
                request.user.save()
                user_to_unfollow.save()

        return HttpResponseRedirect(reverse('account:profile', args=[user_id]))
