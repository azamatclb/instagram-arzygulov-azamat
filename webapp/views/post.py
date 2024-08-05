from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView

from webapp.forms.post import PostForm
from webapp.models import Post

User = get_user_model()


# Create your views here.

class PostListView(LoginRequiredMixin, ListView):
    template_name = 'post_templates/posts.html'
    model = Post
    context_object_name = 'posts'


class PostAddView(LoginRequiredMixin, CreateView):
    template_name = 'post_templates/post_add.html'
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('webapp:posts')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDeleteView(DeleteView):
    template_name = 'post_templates/post_delete.html'
    model = Post
    success_url = reverse_lazy('webapp:posts')


class PostUpdateView(UpdateView):
    template_name = 'post_templates/post_update.html'
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('webapp:posts')

