"""
URL configuration for instagram2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from webapp.views.comment import CommentAddView, CommentDeleteView
from webapp.views.post import PostListView, PostAddView, PostDeleteView, PostUpdateView, PostLikeView, PostDetailView

app_name = 'webapp'
urlpatterns = [
    path('', PostListView.as_view(), name='posts'),
    path('post/add', PostAddView.as_view(), name='post_add'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:post_id>/like/', PostLikeView.as_view(), name='like_post'),
    path('post/<int:pk>/comment/add', CommentAddView.as_view(), name='comment_add'),
    path('post/<int:pk>/view', PostDetailView.as_view(), name='post_comment_view'),
    path('post/<int:post_pk>/comment/<int:comment_pk>/delete/', CommentDeleteView.as_view(), name='comment_delete')

]
