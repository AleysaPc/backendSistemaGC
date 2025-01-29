from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import RegisterViewset, LoginViewset, UserViewset

router = DefaultRouter()
router.register('register', RegisterViewset, basename='register')
router.register('login', LoginViewset, basename='login')
router.register('users', UserViewset, basename='users')

urlpatterns = router.urls