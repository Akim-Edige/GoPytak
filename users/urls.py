from django.urls import path
from users import views as users_views
from orders import views as order_views
from django.contrib.auth.views import LogoutView


app_name = 'users'
urlpatterns = [
    path('login/', users_views.UserLoginView.as_view(), name='login'),
    path('register/', users_views.UserRegistrationView.as_view(), name='register'),
    path("logout/", LogoutView.as_view(), name='logout'),
]
