from django.urls import path
from .views import Register,usernameValidation,emailValidation,passwordValidation,verificationView,LoginView,logoutView,ResetPasswordView,CompletePassword
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register',Register.as_view(),name='register'),
    path('login',LoginView.as_view(),name='login'),
    path('logout',logoutView.as_view(),name='logout'),
    path('validate-username',csrf_exempt(usernameValidation.as_view()),name='user-validation'),
    path('validate-email',csrf_exempt(emailValidation.as_view()),name='email-validation'),
    path('validate-password',csrf_exempt(passwordValidation.as_view()),name='password-validation'),
    path('activate-account/<uidb64>/<token>',verificationView.as_view(),name='activate-account'),
    path('reset-password',ResetPasswordView.as_view(),name='reset-password'),
    path('set-new-password/<uidb64>/<token>',CompletePassword.as_view(),name='reset-user-password'),


]