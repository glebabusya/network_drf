from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import NetworkUser
from .serializers import UserSerializer, UserRegistrationSerializer
from .permissions import IsOwnerOrReadOnly, IsNotAuthenticated


class UserListAPIView(ListAPIView):
    queryset = NetworkUser.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        context = {
            'request': request
        }

        fields = ('id', 'email', 'first_name', 'last_name', 'avatar',
                  'last_login', 'link', 'friend')

        serializer = UserSerializer(queryset, context=context, many=True)

        return Response(serializer.data)


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


class AddFriend(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        user = request.user
        friend = NetworkUser.objects.get(id=id)
        if user.id == friend.id:
            return redirect('user_detail', id)
        user.friend.add(friend)
        friend.friend.add(user)
        user.save()
        friend.save()
        return redirect('user_detail', id)


class LoseFriend(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        user = request.user
        friend = NetworkUser.objects.get(id=id)
        if user.id == friend.id:
            return redirect('user_detail', id)
        user.friend.remove(friend)
        friend.friend.remove(user)
        user.save()
        friend.save()
        return redirect('user_detail', id)
