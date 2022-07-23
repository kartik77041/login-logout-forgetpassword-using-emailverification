from django.urls import path
from accounts import views
urlpatterns = [
    path('', views.home ,name='home'),   
    path('register', views.register_attempt ,name='register_attempt'),   
    path('login', views.login_attempt ,name='login_attempt'),
    path('logout', views.logout_attempt ,name='logout_attempt'),
    path('token', views.token_send ,name='token_send'),
    path('success', views.success ,name='success'),
    path('verify/<auth_token>', views.verify ,name='verify'),
    path('error', views.error_page ,name='error'),
    path('change_password/<token>', views.change_password ,name='change_password'),
    path('forget_password/', views.forget_password ,name='forget_password'),
]