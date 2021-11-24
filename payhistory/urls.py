from django.urls import path
from payhistory import views


urlpatterns = [
    path('histories/', views.HistoryList.as_view(), name='history_list'),
    path('histories/', views.HistoryList.as_view(), name='insert_history'),
    path('histories/<int:id>', views.HistoryDetail.as_view(), name='update_history'),
    path('histories/<int:id>', views.HistoryDetail.as_view(), name='delete_history'),
]
