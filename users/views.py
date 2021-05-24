from django.shortcuts import redirect
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView, CreateAPIView
from rest_framework.response import Response

from .models import NetworkUser
from .serializers import UserSerializer, UserRegistrationSerializer
from .permissions import IsOwnerOrReadOnly, IsNotAuthenticated


class UserListAPIView(ListAPIView):
    queryset = NetworkUser.objects.all()
    serializer_class = UserSerializer


class UserDetailAPIView(RetrieveUpdateAPIView):
    queryset = NetworkUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrReadOnly]


class UserRegistrationAPIView(CreateAPIView):
    queryset = NetworkUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [IsNotAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = True
            return redirect('user_list')
        else:
            data = serializer.errors
            return Response(data)
