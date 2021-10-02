from django.urls import path

from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('dashboard/', views.dashBoard, name='dashboard'),
    path('login/', views.loginUser, name='login'),
    path('register/', views.registerUser, name='register'),
    path('profile/', views.userProfile, name='profile'),
    path('error/', views.dashBoardErrorPage, name='error'),
    path('reset_password/', views.resetPassword, name='forgotpassword'),
    path('no_page/', views.generalErrorPage, name='err'),
    path('logout/', views.logoutUser, name='logout'),
    path('password/', views.changePassword, name='changepassword'),
    path('notifications/', views.notificationPage, name='notifications'),
    path('tasks/', views.taskBoard, name='taskboard')
]
