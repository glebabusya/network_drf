from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import NoteSerializer, CommentSerializer
from .models import Note, Comment
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsAuthorOrReadOnly


class NoteListAPIView(ListCreateAPIView):
    queryset = Note.objects.all().order_by('uploaded_time')
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class NoteDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all().order_by('uploaded_time')
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]


class CommentListAPIView(ListCreateAPIView):
    queryset = Comment.objects.all().order_by('uploaded_time')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CommentDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all().order_by('uploaded_time')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
