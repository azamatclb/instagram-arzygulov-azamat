from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView

from apps.account.models import Profile
from apps.webapp.forms.comment import CommentForm
from apps.webapp.forms.like import LikeForm
from apps.webapp.forms.post import PostForm
from apps.webapp.models import Post

User = get_user_model()


# Create your views here.

class PostListView(LoginRequiredMixin, ListView):
    template_name = 'post_templates/posts.html'
    model = Post
    context_object_name = 'posts'
    ordering = "-created_at"

    # def get_queryset(self):
    #     user = self.request.user
    #     if not hasattr(user, 'profile'):
    #         return Post.objects.none()
    #
    #     followed_profiles = Profile.objects.filter(following__follower=user.profile)
    #
    #     # queryset = Post.objects.filter(author__in=followed_profiles).order_by('-created_at')
    #     return queryset

    def get_queryset(self):
        return Post.objects.all().order_by('-created_at')


class PostAddView(LoginRequiredMixin, CreateView):
    template_name = 'post_templates/post_add.html'
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('webapp:posts')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'post_templates/post_delete.html'
    model = Post
    success_url = reverse_lazy('webapp:posts')


class PostUpdateView(UpdateView):
    template_name = 'post_templates/post_update.html'
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('webapp:posts')


class PostDetailView(LoginRequiredMixin, DetailView):
    template_name = 'post_templates/post_view.html'
    context_object_name = 'post'
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['comments'] = post.comment.all()
        context['form'] = CommentForm()
        return context


class PostLikeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        post_id = kwargs.get('pk')
        form = LikeForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post_id')
            post = get_object_or_404(Post, id=post_id)

        if request.user not in post.liked_by.all():
            post.liked_by.add(request.user)
            post.likes_count += 1
            post.save()
        else:
            post.liked_by.remove(request.user)
            post.likes_count -= 1
            post.save()

        return redirect('webapp:post_comment_view', pk=post_id)
