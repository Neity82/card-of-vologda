from django.contrib.auth.views import LogoutView, PasswordChangeView
from django.urls import path

from app_user.views import LoginUser, СitizenAccount, Profile, HistoryView, \
    password_change_done, RegisterUser, ОrganizationAccount, Verify, Accrue, Deduct

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/citizen_account/', СitizenAccount.as_view(), name='citizen_account'),
    path('profile/<int:pk>/organization_account/', ОrganizationAccount.as_view(), name='organization_account'),
    path('profile/<int:pk>/profile/', Profile.as_view(), name='profile'),
    path('profile/<int:pk>/history/', HistoryView.as_view(), name='history'),
    path('profile/<int:pk>/verify/', Verify.as_view(), name='verify'),
    path('profile/<int:pk>/accrue/', Accrue.as_view(), name='accrue'),
    path('profile/<int:pk>/deduct/', Deduct.as_view(), name='deduct'),
    path('password-change/', PasswordChangeView.as_view(template_name='app_user/password_change.html'),
         name='password_change'),
    path('password-change/done/', password_change_done, name='password_change_done'),
    path('register/', RegisterUser.as_view(), name='register'),

]
