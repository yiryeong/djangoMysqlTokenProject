from django.urls import path
from user import views


urlpatterns = [
    path('list/', views.GetUserList.as_view(), name='get_user_list'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
]
