from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('account/',views.account,name='account'),
    path('profile_update/',views.profile_update,name='profile_update'),
    path('logout/',views.logout,name='logout'),
    path('changepassword/',views.changepassword,name='changepassword'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),
    # path('error/', views.error, name='error'),
    #admin dashborad 
    # path('index/',views.index,name='index'),

]

# handler404 = 'logapp.views.error'
# path('home/',views.home,name='home'),