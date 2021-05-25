from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.UserListAPIView.as_view(), name='user_list'),
    path('<int:pk>', views.UserDetailAPIView.as_view(), name='user_detail'),
    path('registration', views.UserRegistrationAPIView.as_view(), name='registration'),
    path('login/', include('rest_framework.urls')),
    path('add-friend/<int:id>', views.AddFriend.as_view(), name='add_friend'),
    path('lose-friend/<int:id>', views.LoseFriend.as_view(), name='lose_friend')
]