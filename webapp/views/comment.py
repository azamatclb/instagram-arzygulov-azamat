from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView
from webapp.forms.comment import CommentForm
from webapp.models import Comment, Post


class CommentAddView(LoginRequiredMixin, CreateView):
    template_name = 'comment_templates/comment_add.html'
    model = Comment
    form_class = CommentForm
    success_url = 'webapp:posts'

    def form_valid(self, form):
        form.instance.author = self.request.user
        pk = self.kwargs.get('pk')
        post = get_object_or_404(Post, id=pk)
        form.instance.post = post
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs.get('pk')
        return reverse_lazy('webapp:post_comment_view', kwargs={'pk': pk})


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'comment_templates/comment_delete.html'
    success_url = reverse_lazy('webapp:posts')

    def get_object(self, queryset=None):
        post_pk = self.kwargs.get('post_pk')
        comment_pk = self.kwargs.get('comment_pk')
        return get_object_or_404(Comment, pk=comment_pk, post_id=post_pk)
