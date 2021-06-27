from django.urls import path
from . import views

urlpatterns = [
    path('', views.NoteListAPIView.as_view(), name='note_list'),
    path('<int:pk>', views.NoteDetailAPIView.as_view(), name='note_detail'),
    path('comments/', views.CommentListAPIView.as_view(), name='comment_list'),
    path('comments/<int:pk>', views.CommentDetailAPIView.as_view(), name='comment_detail')
]
