from django.urls import path
from payhistory import views


urlpatterns = [
    path('getuserlist/', views.GetUserList.as_view(), name='get_user_list'),
    path('register/', views.RegistUser.as_view(), name='register'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('history/getlist/', views.HistoryList.as_view(), name='history_list'),
    path('history/insert/', views.CreateHistory.as_view(), name='insert_history'),
    path('history/update/<int:id>', views.UpdateHistory.as_view(), name='update_history'),
    path('history/delete/<int:id>', views.DeleteHistory.as_view(), name='delete_history'),
]
