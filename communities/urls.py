from django.urls import path
from . import views
urlpatterns = [
    path('', views.CommunityListAPIView.as_view(), name='community_list'),
    path('<slug:slug>', views.CommunityDetailAPIView.as_view(), name='community_detail'),
    path('<slug:slug>/subscribe', views.Subscribe.as_view(), name='subscribe'),
    path('<slug:slug>/unsubscribe', views.UnSubscribe.as_view(), name='unsubscribe')

]