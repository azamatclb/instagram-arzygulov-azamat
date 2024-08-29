from django.urls import path, include
from rest_framework import routers
from api_v1.views import PostViewSet
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth.views import LogoutView

app_name = 'api_v1'

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)
# router.register('')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', obtain_auth_token, name='api_token_auth'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
