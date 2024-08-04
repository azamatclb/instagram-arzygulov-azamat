from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView


# Create your views here.


def posts_view(request):
    if request.method == "GET":
        return render(request, 'posts.html')
